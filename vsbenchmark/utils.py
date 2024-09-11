from typing import Any, Dict, Self
import psutil
import os
import time
import json

from enum import Flag, auto


class Logger:
    def __init__(self: Self):
        self.current_process = psutil.Process(os.getpid())

    def log_start(self: Self):
        self.current_process.cpu_percent()
        self.start_time = time.perf_counter()
        self.start_cpu_time = time.process_time()

    def log_end(self: Self) -> Dict[str, Any]:
        end_time = time.perf_counter()
        end_cpu_time = time.process_time()

        elapsed_time = end_time - self.start_time
        cpu_time = end_cpu_time - self.start_cpu_time
        cpu_percent = self.current_process.cpu_percent()
        memory_info = self.current_process.memory_info()
        memory_usage = memory_info.rss / 1024 / 1024

        return {
            "elapsed_time": elapsed_time,
            "cpu_time": cpu_time,
            "cpu_percent": cpu_percent,
            "memory_usage": memory_usage,
            "fps": 1 / elapsed_time if elapsed_time > 0 else 0
        }


class Results:
    @staticmethod
    def save_results(results: Dict, filename: str, overwrite: bool = False) -> None:
        if os.path.exists(filename) and not overwrite:
            raise FileExistsError(f"The file '{filename}' already exists.")

        serialized_results = Results.serialize_results(results)
        with open(filename, 'w') as f:
            json.dump(serialized_results, f, indent=2)

    @staticmethod
    def load_results(filename: str) -> Dict:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        with open(filename, 'r') as f:
            loaded_data = json.load(f)
        return Results.deserialize_results(loaded_data)

    @staticmethod
    def serialize_results(results: Dict) -> Dict:
        serialized = {}

        for func_params, resolutions in results.items():
            serialized[func_params] = {}
            for resolution, formats in resolutions.items():
                serialized[func_params][str(resolution)] = {}
                for format, thread_results in formats.items():
                    serialized[func_params][str(resolution)][format.name] = {
                        str(threads): {metric.name: value for metric, value in results.items()}
                        for threads, results in thread_results.items()
                    }

        return serialized

    @staticmethod
    def deserialize_results(data: Dict) -> Dict:
        from vstools import vs
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


class Metric(Flag):
    TIME = auto()
    FPS = auto()
    CPU_USAGE = auto()
    MEMORY_USAGE = auto()
    PERFORMANCE_EFFICIENCY = auto()
    THREADING_EFFICIENCY = auto()
    ALL = TIME | FPS | THREADING_EFFICIENCY | PERFORMANCE_EFFICIENCY | CPU_USAGE | MEMORY_USAGE
