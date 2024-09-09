from typing import Any, Dict, Self
import psutil
import os
import time

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


class Metric(Flag):
    TIME = auto()
    FPS = auto()
    EFFICIENCY = auto()
    CPU_USAGE = auto()
    MEMORY_USAGE = auto()
    ALL = TIME | FPS | EFFICIENCY | CPU_USAGE | MEMORY_USAGE
