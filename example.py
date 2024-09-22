from vstools import vs, core
from vsrgtools import box_blur

from vsbenchmark import VSBenchmark, Metric

functions = {
    "std boxblur": core.std.BoxBlur,
    "avx boxblur": core.box.Blur,
    "zig boxblur": core.zboxblur.Blur,
    "zip boxblur": core.vszip.BoxBlur,
    "jet boxblur": box_blur,
}

_range = list(range(1, 2))

params = {
    'hpasses': _range,
    'vpasses': _range,
    'hradius': _range,
    'vradius': _range,
}

tests = {
    "jet boxblur": {
        vs.YUV:     {'radius': 1, 'passes': 1},
        vs.RGB:     {'radius': 1, 'passes': 1},
        vs.GRAY:    {'radius': 1, 'passes': 1},
    },
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
    resolutions=[(1920, 1080)],
    length=500,
    passes=3,
    param_grid=params,
    tests=tests,
)

# In the case that you want to pass your own args, usage is simple
benchmark = VSBenchmark(
    functions={
        "std boxblur": lambda x: core.std.BoxBlur(x, hpasses=2, vpasses=2),
        "zip boxblur": lambda x: core.vszip.BoxBlur(x, hpasses=2, vpasses=2)
    },
    formats=[vs.GRAY16, vs.GRAYS],
    resolutions=[(1920, 1080), (3840, 2160)],
    length=500,
    passes=3
)

benchmark.run_benchmark()
benchmark.display_results()
benchmark.compare_functions(Metric.FPS)