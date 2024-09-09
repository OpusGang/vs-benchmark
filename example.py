import itertools
from vstools import vs, core
from vsrgtools import box_blur
from vsbenchmark import VSBenchmark, Metric

_range = range(1, 2)


def box_blur_generator() -> list[dict[str, int]]:
    passes = _range
    radii = _range
    return [{'passes': p, 'radius': r} for p, r in itertools.product(passes, radii)]


param_grid = {
    'hpasses': list(_range),
    'vpasses': list(_range),
    'hradius': list(_range),
    'vradius': list(_range),
    'passes': list(_range),
    'radius': list(_range)
}

param_mapping = {
    "std boxblur": ['hpasses', 'vpasses', 'hradius', 'vradius'],
    "avx boxblur": ['hpasses', 'vpasses', 'hradius', 'vradius'],
    "zig boxblur": ['hpasses', 'vpasses', 'hradius', 'vradius'],
    "zip boxblur": ['hpasses', 'vpasses', 'hradius', 'vradius'],
    "jet boxblur": box_blur_generator
}

functions = {
    "std boxblur": lambda x, params: core.std.BoxBlur(x, **params),
    "avx boxblur": lambda x, params: core.box.Blur(x, **params),
    "zig boxblur": lambda x, params: core.zboxblur.Blur(x, **params),
    "zip boxblur": lambda x, params: core.vszip.BoxBlur(x, **params),
    "jet boxblur": lambda x, params: box_blur(x, **params)
}

# I am generally of the thought that when testing function performance
# it is best to use either a single thread or a controlled number of threads
# There are too many potential issues when testing fast functions across
# many threads. This is less of a problem when testing
# compute heavy filters (BM3D) where thread vs FPS scaling is more linear.

# Consider set_affinity:
# core.set_affinity(threads=range(0, 32, 2), max_cache=22000)

core.num_threads = 1

benchmark = VSBenchmark(
    functions=functions,
    formats=[vs.GRAY16, vs.GRAYS],
    resolutions=[(1920, 1080), (3840, 2160)],
    length=240,
    dynamic_length=True,
    max_threads=None,
    passes=3,
    param_grid=param_grid,
    param_mapping=param_mapping,
)


# Run benchmark and save data to json
benchmark.run_benchmark()
benchmark.save_results('benchmark_results.json', overwrite=True)

# Display results for specific metrics
benchmark.display_results(Metric.TIME | Metric.FPS | Metric.CPU_USAGE)

# Display best funciton
benchmark.compare_functions(Metric.FPS)

# Load existing data and compare functions based on FPS
# benchmark.load_results('benchmark_results.json')
# benchmark.compare_functions(Metric.FPS)
