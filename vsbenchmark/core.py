import json
from typing import Any, Callable, Dict, List, Optional, Self, Tuple, Union
from vstools import vs, core, clip_async_render
from dataclasses import dataclass, field
import itertools
import os
from tabulate import tabulate

from .utils import Logger, Metric


@dataclass
class VSBenchmark:
    functions: Dict[str, Callable[[vs.VideoNode, Dict[str, Any]], vs.VideoNode]]
    formats: List[int] = field(default_factory=lambda: [vs.GRAYS])
    resolutions: List[Tuple[int, int]] = field(default_factory=lambda: [(1280, 720), (1920, 1080), (3840, 2160)])
    passes: int = 3
    max_threads: Optional[int] = None
    length: int = 240
    dynamic_length: bool = False
    param_grid: Optional[Dict[str, Union[List[float], List[int]]]] = None
    param_mapping: Optional[Dict[str, Union[List[str], Callable[[], List[Dict[str, Any]]]]]] = None

    def __post_init__(self: Self) -> None:
        self._results = {}
        self._single_thread_time = None
        if self.dynamic_length:
            self.base_resolution = min(self.resolutions, key=lambda r: r[0] * r[1])

        if self.param_grid is None:
            self.param_grid = {}

        if self.param_mapping is None:
            self.param_mapping = {func_name: list(self.param_grid.keys()) for func_name in self.functions}
        elif not self.param_mapping:
            self.param_mapping = {func_name: [] for func_name in self.functions}

    def _generate_thread_counts(self: Self) -> List[int]:
        if self.max_threads is None:
            return [core.num_threads]

        base_counts = [1, 2, 4, 6, 8, 12, 16]
        return sorted(set(count for count in itertools.chain(base_counts, range(24, self.max_threads + 1, 8)) 
                          if count <= self.max_threads))

    def _generate_param_combinations(self: Self, func_name: str) -> List[Dict[str, Any]]:
        mapping = self.param_mapping.get(func_name, [])

        if callable(mapping):
            return mapping()

        if not mapping:
            return [{}]

        relevant_params = {k: v for k, v in self.param_grid.items() if k in mapping}
        return [dict(zip(relevant_params.keys(), v)) for v in itertools.product(*relevant_params.values())]

    def _calculate_length(self: Self, resolution: Tuple[int, int]) -> int:
        if not self.dynamic_length:
            return self.length

        base_pixels = self.base_resolution[0] * self.base_resolution[1]
        resolution_pixels = resolution[0] * resolution[1]
        resolution_factor = base_pixels / resolution_pixels

        # Always return at least 1 frame
        return max(1, round(self.length * resolution_factor))

    def run_benchmark(self: Self) -> None:
        thread_counts = self._generate_thread_counts()
        logger = Logger()

        for resolution in self.resolutions:
            length = self._calculate_length(resolution)
            for format in self.formats:
                for func_name, func in self.functions.items():
                    param_combinations = self._generate_param_combinations(func_name)
                    for params in param_combinations:
                        result_key = f"{func_name}_{params}" if params else func_name
                        self._results.setdefault(result_key, {}).setdefault(resolution, {}).setdefault(format, {})

                        for thread_count in thread_counts:
                            if self.max_threads is not None:
                                core.num_threads = thread_count

                            passes_data = []
                            for _ in range(self.passes):
                                print(f"running {resolution}, frames={length}, {func_name, params}, threads={thread_count}, pass={_}            ", end="\r")  # type: ignore

                                clip = core.std.BlankClip(width=resolution[0], height=resolution[1], format=format, length=length, keep=False)
                                logger.log_start()
                                clip_async_render(func(clip, params))
                                passes_data.append(logger.log_end())

                            metrics = self._calculate_metrics(passes_data, thread_count, self._single_thread_time, length)
                            self._results[result_key][resolution][format][thread_count] = metrics

                            if thread_count == 1:
                                self._single_thread_time = metrics[Metric.TIME]

    def _calculate_metrics(self: Self, passes_data: List[Dict[str, float]], thread_count: int, single_thread_time: Optional[float], length: int) -> Dict[Metric, float]:
        avg_time = sum(pass_data['elapsed_time'] for pass_data in passes_data) / len(passes_data)
        return {
            Metric.TIME: avg_time,
            Metric.FPS: length / avg_time,
            Metric.EFFICIENCY: (single_thread_time / avg_time) / thread_count if single_thread_time and thread_count > 1 else 1.0,
            Metric.CPU_USAGE: sum(pass_data['cpu_percent'] for pass_data in passes_data) / len(passes_data),
            Metric.MEMORY_USAGE: sum(pass_data['memory_usage'] for pass_data in passes_data) / len(passes_data)
        }

    def save_results(self: Self, filename: str, overwrite: bool = False) -> None:
        """
        Save the benchmark results to a JSON file.

        Args:
            filename (str): The name of the file to save the results to.
            overwrite (bool): If True, overwrite the file if it exists. If False, raise an error if the file exists. Defaults to False.

        Raises:
            FileExistsError: If the file already exists and overwrite is False.
        """
        if os.path.exists(filename) and not overwrite:
            raise FileExistsError(f"The file '{filename}' already exists. Use overwrite=True to overwrite it.")

        serialized_results = self._serialize_results()
        with open(filename, 'w') as f:
            json.dump(serialized_results, f, indent=2)

    def _serialize_results(self: Self) -> Dict:
        """
        Convert the results to a JSON-serializable format.

        Returns:
            Dict: A dictionary containing the serialized benchmark results.
        """
        serialized = {}
        for func_params, resolutions in self._results.items():
            serialized[func_params] = {}
            for resolution, formats in resolutions.items():
                serialized[func_params][str(resolution)] = {}
                for format, thread_results in formats.items():
                    serialized[func_params][str(resolution)][format.name] = {
                        str(threads): {metric.name: value for metric, value in results.items()}
                        for threads, results in thread_results.items()
                    }
        return serialized

    def load_results(self: Self, filename: str) -> None:
        """
        Load benchmark results from a JSON file.

        Args:
            filename (str): The name of the file to load the results from.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        self._results = self._deserialize_results(loaded_data)

    def _deserialize_results(self: Self, data: Dict) -> Dict:
        """
        Convert the loaded data back to the original format.

        Args:
            data (Dict): The loaded data from the JSON file.

        Returns:
            Dict: A dictionary containing the deserialized benchmark results.
        """
        deserialized = {}
        for func_params, resolutions in data.items():
            deserialized[func_params] = {}
            for resolution_str, formats in resolutions.items():
                resolution = tuple(map(int, resolution_str.strip('()').split(', ')))
                deserialized[func_params][resolution] = {}
                for format_name, thread_results in formats.items():
                    format = getattr(vs, format_name)
                    deserialized[func_params][resolution][format] = {
                        int(threads): {Metric[metric]: value for metric, value in results.items()}
                        for threads, results in thread_results.items()
                    }
        return deserialized

    def display_results(self: Self, metrics: Metric = Metric.ALL) -> None:
        """
        Display the benchmark results in a tabular format, grouped by resolution and format.

        Args:
            metrics (Metric): Metrics to display. Defaults to Metric.ALL.
        """
        metric_list: list[Metric] = [m for m in Metric if m in metrics and m != Metric.ALL]
        headers: list[str] = ['Function', 'Parameters', 'Threads'] + [m.name for m in metric_list]

        for resolution, formats in self._get_sorted_results():
            print(f"\nResolution: {resolution[0]}x{resolution[1]}")

            for format, results in formats.items():
                print(f"\nFormat: {format.name}")

                table_data = []
                for func_params, thread_results in results.items():
                    func_name, params_str = func_params.split('_', 1) if '_' in func_params else (func_params, '{}')
                    params = eval(params_str)

                    for threads, metric_results in thread_results.items():
                        row = [
                            func_name,
                            ', '.join(f'{k}={v}' for k, v in params.items()),
                            threads
                        ]
                        row.extend([f"{metric_results[metric]:.2f}" for metric in metric_list])
                        table_data.append(row)

                print(tabulate(table_data, headers=headers, tablefmt='simple'))
                print()

    def _get_sorted_results(self: Self) -> List[Tuple[Tuple[int, int], Dict]]:
        """
        Sort and restructure the results for easier display.

        Returns:
            List[Tuple[Tuple[int, int], Dict]]: Sorted list of (resolution, formats) tuples.
        """
        sorted_results = []
        for resolution in sorted(set(res for func in self._results.values() for res in func.keys())):
            formats = {}
            for format in sorted(set(fmt for func in self._results.values() for fmt in func[resolution].keys()), key=lambda f: f.name):
                format_results = {}
                for func_params, func_results in self._results.items():
                    if resolution in func_results and format in func_results[resolution]:
                        format_results[func_params] = func_results[resolution][format]
                formats[format] = format_results
            sorted_results.append((resolution, formats))
        return sorted_results

    def compare_functions(self: Self, metric: Metric = Metric.FPS) -> None:
        """
        Compare functions and find the best one for each format and resolution based on a specific metric.
        For FPS and EFFICIENCY, higher is better. For other metrics, lower is better.
        """
        if metric == Metric.ALL or metric not in Metric:
            raise ValueError("Please specify a single metric for comparison")

        comparison_data = {}
        is_higher_better = metric in {Metric.FPS, Metric.EFFICIENCY}

        for func_params, resolutions in self._results.items():
            func_name, params_str = func_params.split('_', 1) if '_' in func_params else (func_params, '{}')
            params = eval(params_str)

            for resolution, formats in resolutions.items():
                for format, thread_results in formats.items():
                    key = (resolution, format.name)
                    if key not in comparison_data:
                        comparison_data[key] = {'best_value': None, 'best_func': None, 'best_params': None, 'best_thread': None}

                    for thread_count, results in thread_results.items():
                        value = results[metric]
                        current_best = comparison_data[key]['best_value']

                        if (current_best is None or 
                            (is_higher_better and value > current_best) or
                            (not is_higher_better and value < current_best)):
                            comparison_data[key] = {
                                'best_value': value,
                                'best_func': func_name,
                                'best_params': params,
                                'best_thread': thread_count
                            }

        headers = ['Resolution', 'Format', 'Best Function', 'Best Parameters', 'Best Thread Count', f'Best {metric.name}']
        table_data = []

        for (resolution, format), data in comparison_data.items():
            row = [
                f'{resolution[0]}x{resolution[1]}',
                format,
                data['best_func'],
                ', '.join(f'{k}={v}' for k, v in data['best_params'].items()) if data['best_params'] else 'N/A',
                data['best_thread'],
                f"{data['best_value']:.2f}"
            ]
            table_data.append(row)

        print(f"\nBest Functions Comparison ({metric.name}):")
        print(tabulate(table_data, headers=headers, tablefmt='simple'))
