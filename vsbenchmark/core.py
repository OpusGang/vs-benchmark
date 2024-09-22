import itertools
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import time
import logging
import inspect

import pandas as pd
from tqdm import tqdm
from tabulate import tabulate

from vstools import vs, core, clip_async_render, get_color_family

from .utils import Metric

logging.basicConfig(
    level=logging.INFO,
    filename='benchmark.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VSBenchmark:
    def __init__(
        self,
        functions: Dict[str, Callable[..., vs.VideoNode]],
        formats: List[int],
        resolutions: List[Tuple[int, int]],
        length: int = 240,
        passes: int = 3,
        param_grid: Optional[Dict[str, Union[List[Any], Any]]] = None,
        tests: Optional[Dict[str, Dict[Union[int, vs.ColorFamily], Dict[str, Union[List[Any], Any]]]]] = None,
        list_params: Optional[List[str]] = None
    ):

        self.functions = functions
        self.passes = passes if passes else 3
        self.formats = formats
        self.resolutions = resolutions
        self.length = length
        self.param_grid = param_grid if param_grid else {}
        self.tests = tests if tests is not None else {}
        self.list_params = list_params if list_params is not None else ['planes']

        self.results = pd.DataFrame()

    def generate_test_cases(self) -> List[Dict]:
        test_cases = []

        for func_name, func in self.functions.items():
            for fmt in self.formats:
                color_family = get_color_family(fmt)

                applicable_tests = {}
                if func_name in self.tests:

                    specific_format_test = self.tests[func_name].get(fmt, None)
                    if specific_format_test:
                        applicable_tests = specific_format_test.copy()

                    if not applicable_tests:
                        family_test = self.tests[func_name].get(color_family, None)
                        if family_test:
                            applicable_tests = family_test.copy()

                if applicable_tests:
                    applicable_parameters = applicable_tests
                else:
                    applicable_parameters = self.param_grid.copy()

                normalized_params = self._normalize_params(applicable_parameters)

                extracted_list_params = {k: v for k, v in normalized_params.items() if k in self.list_params}
                other_params = {k: v for k, v in normalized_params.items() if k not in self.list_params}

                for k, v in other_params.items():
                    if not isinstance(v, list):
                        other_params[k] = [v]

                if other_params:
                    keys = list(other_params.keys())
                    values = [other_params[key] for key in keys]

                    for combination in itertools.product(*values):
                        param_dict = dict(zip(keys, combination))
                        for k, v in extracted_list_params.items():
                            param_dict[k] = v

                        if not self.validate_function_params(func, param_dict, fmt):
                            logging.error(f"Function '{func_name}' cannot accept parameters {param_dict}. Skipping test case.")
                            print(f"Error: Function '{func_name}' cannot accept parameters {param_dict}. Skipping test case.")
                            continue

                        test_case = {
                            'test_name': func_name,
                            'function': func,
                            'params': param_dict,
                            'format': fmt
                        }
                        test_cases.append(test_case)
                else:
                    param_dict = {}
                    for k, v in extracted_list_params.items():
                        param_dict[k] = v

                    if not self.validate_function_params(func, param_dict, fmt):
                        logging.error(f"Function '{func_name}' cannot accept parameters {param_dict}. Skipping test case.")
                        print(f"Error: Function '{func_name}' cannot accept parameters {param_dict}. Skipping test case.")
                        continue

                    test_case = {
                        'test_name': func_name,
                        'function': func,
                        'params': param_dict,
                        'format': fmt
                    }
                    test_cases.append(test_case)

        return test_cases

    def _normalize_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {}
        for k, v in params.items():
            if isinstance(v, dict):
                logging.warning(f"Parameter '{k}' is a dictionary. It will be treated as a single parameter.")
                normalized[k] = v
            elif not isinstance(v, list) and k not in self.list_params:
                normalized[k] = [v]
            else:
                normalized[k] = v

        return normalized

    def validate_function_params(self, func: Callable, params: Dict[str, Any], fmt: int) -> bool:
        try:
            sig = inspect.signature(func)
            if 'format' in params:
                dummy_clip = core.std.BlankClip(format=params['format'], length=self.length)
            else:
                dummy_clip = core.std.BlankClip(format=fmt, length=self.length)
            sig.bind(dummy_clip, **params)
            return True
        except TypeError as e:
            logging.error(f"Parameter binding failed for function '{func.__name__}': {e}")
            return False

    def benchmark_function(self, func: Callable, clip: vs.VideoNode, params: Dict[str, Any]) -> Tuple[float, float]:
        # perf_counter doesn't match asnyc_render
        start_time = time.time()

        # not sure if puttingt logging within time.time is ideal xd
        try:
            processed_clip = func(clip, **params)
            clip_async_render(processed_clip)
        except Exception as e:
            logging.error(f"Error processing function '{func.__name__}' with params {params}: {e}")
            raise e

        end_time = time.time()

        elapsed_time = end_time - start_time
        fps = self.length / elapsed_time if elapsed_time > 0 else float('inf')
        return elapsed_time, fps

    def run_benchmark(self):
        test_cases = self.generate_test_cases()

        format_to_test_cases = {}
        for test_case in test_cases:
            fmt = test_case['format']
            if fmt not in format_to_test_cases:
                format_to_test_cases[fmt] = []
            format_to_test_cases[fmt].append(test_case)

        total_tests = 0
        for resolution in self.resolutions:
            for fmt in self.formats:
                applicable_test_cases = format_to_test_cases.get(fmt, [])
                total_tests += len(applicable_test_cases) * self.passes

        if total_tests == 0:
            print("No test cases to run.")
            return

        bar_format = 'Progress: {percentage:3.0f}%|{bar:30}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'

        results = []
        try:
            # why doesn't this have a decorator wtf
            with tqdm(total=total_tests, unit="test", bar_format=bar_format) as pbar:
                for resolution in self.resolutions:
                    width, height = resolution
                    for fmt in self.formats:
                        # hmmm...
                        fmt_name = str(fmt.name) # type: ignore

                        applicable_test_cases = format_to_test_cases.get(fmt, [])
                        if not applicable_test_cases:
                            logging.warning(f"No test cases found for format {fmt_name}. Skipping.")
                            continue

                        try:
                            clip = core.std.BlankClip(width=width, height=height, format=fmt, length=self.length)
                        except Exception as e:
                            logging.error(f"Failed to create BlankClip with resolution {resolution} and format {fmt_name}: {e}")
                            print(f"Error: Failed to create BlankClip with resolution {resolution} and format {fmt_name}: {e}")

                            pbar.update(len(applicable_test_cases) * self.passes)
                            continue

                        for test_case in applicable_test_cases:
                            func_name = test_case['test_name']
                            func = test_case['function']
                            params = test_case['params']

                            for pass_num in range(self.passes):
                                current_test = f"Function: {func_name}, Params: {params}, Pass: {pass_num + 1}"
                                pbar.set_postfix_str(current_test)
                                try:
                                    elapsed_time, fps = self.benchmark_function(func, clip, params)
                                    results.append({
                                        'Function': func_name,
                                        'Resolution': f'{width}x{height}',
                                        'Format': fmt_name,
                                        'Params': str(params),
                                        'Pass': pass_num + 1,
                                        'Time': elapsed_time,
                                        'FPS': fps
                                    })
                                    logging.info(f"Test: {func_name}, Params: {params}, Resolution: {resolution}, Format: {fmt_name}, Pass: {pass_num + 1}, Time: {elapsed_time:.4f}s, FPS: {fps:.2f}")
                                except Exception as e:
                                    logging.error(f"Error in Test: {func_name}, Params: {params}, Resolution: {resolution}, Format: {fmt_name}, Pass: {pass_num + 1} - {e}")

                                    results.append({
                                        'Function': func_name,
                                        'Resolution': f'{width}x{height}',
                                        'Format': fmt_name,
                                        'Params': str(params),
                                        'Pass': pass_num + 1,
                                        'Time': float('nan'),
                                        'FPS': float('nan')
                                    })
                                pbar.update(1)

        except KeyboardInterrupt:
            logging.warning("Benchmarking interrupted by user.")
            print("Benchmarking interrupted by user.")
        finally:
            self.results = pd.DataFrame(results)

    def display_results(self):
        if self.results.empty:
            print("No results to display.")
            return

        grouped = self.results.groupby(['Resolution', 'Format', 'Function', 'Params'])
        summary = grouped.agg({
            'Time': ['min', 'max', 'mean'],
            'FPS': ['min', 'max', 'mean']
        }).reset_index()
        summary.columns = ['Resolution', 'Format', 'Function', 'Params', 'Time_Min', 'Time_Max', 'Time_Avg', 'FPS_Min', 'FPS_Max', 'FPS_Avg']

        function_order = {func: i for i, func in enumerate(self.functions.keys())}
        summary['sort_key'] = summary['Function'].map(function_order)  # type: ignore

        for resolution in summary['Resolution'].unique():
            print(f"\nResolution: {resolution}\n")
            for format in summary['Format'].unique():
                print(f"Format: {format}")

                data = summary[(summary['Resolution'] == resolution) & (summary['Format'] == format)].copy()

                if data.empty:
                    print("No data available for this format.")
                    continue

                best_time = data['Time_Avg'].min()
                data['Relative'] = best_time / data['Time_Avg']

                data = data.sort_values('sort_key')  # type: ignore

                table_data = []
                for _, row in data.iterrows():
                    table_data.append([
                        row['Function'],
                        row['Params'],
                        # // TODO
                        # it would be super poggers if {.2f} was dynamic based on the largest result
                        # this woud ensure a consistent table size
                        # TO AVOID THIS:
                        # 692.73 [677.52, 711.99]
                        # 1178.32 [1097.38, 1262.42]
                        #
                        # with dynamic formatting
                        # 692.730 [677.520, 711.990]
                        # 1178.32 [1097.38, 1262.42]
                        f"{row['Time_Avg']:.2f} [{row['Time_Min']:.2f}, {row['Time_Max']:.2f}]",
                        f"{row['FPS_Avg']:.2f} [{row['FPS_Min']:.2f}, {row['FPS_Max']:.2f}]",
                        f"{row['Relative']:.2f}"
                    ])

                headers = ['Function', 'Params', 'Time [min, max]', 'FPS [min, max]', 'Relative']
                print(tabulate(table_data, headers=headers, tablefmt="simple"))
                print()

    def compare_functions(self, metric: Metric):
        if metric not in [Metric.TIME, Metric.FPS]:
            raise ValueError("Invalid metric for comparison. Choose Metric.TIME or Metric.FPS.")

        if self.results.empty:
            print("No results to compare.")
            return

        metric_name = metric.value

        grouped = self.results.groupby(['Resolution', 'Format', 'Function', 'Params'])
        summary = grouped[metric_name].mean().reset_index()

        best_functions = summary.copy()
        if metric == Metric.TIME:
            best_functions['Rank'] = best_functions.groupby(['Resolution', 'Format'])[metric_name].rank(
                ascending=True, method='min'
            )
        else:
            best_functions['Rank'] = best_functions.groupby(['Resolution', 'Format'])[metric_name].rank(
                ascending=False, method='min'
            )
        best_functions = best_functions[best_functions['Rank'] == 1]

        headers = ['Resolution', 'Format', 'Best Function', 'Best Parameters', f'Best {metric_name}']
        table_data = best_functions[['Resolution', 'Format', 'Function', 'Params', metric_name]].values.tolist()

        print(f"\nBest Functions Comparison ({metric_name}):")
        print(tabulate(table_data, headers=headers, tablefmt="simple", floatfmt=".2f"))
        print()

    def save_results(self, filename: str):
        if self.results.empty:
            print("No results to export.")
            return
        try:
            export_df = self.results.copy()
            export_df['Format'] = export_df['Format'].apply(lambda x: x if isinstance(x, str) else str(x))
            export_df['Params'] = export_df['Params'].apply(lambda x: x if isinstance(x, str) else str(x))
            export_df.to_csv(filename, index=False)
            print(f"Results exported to {filename}")
            logging.info(f"Results exported to {filename}")
        except Exception as e:
            logging.error(f"Failed to export results to CSV: {e}")
            print(f"Error: Failed to export results to CSV: {e}")

    def get_results(self) -> pd.DataFrame:
        return self.results
