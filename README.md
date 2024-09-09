# vs-benchmark
Moderately extensive tool for benchmarking Vapoursynth functions en masse

## Limitations and considerations

1. **Problem**: Memory usage is not garbage collected (GC'd) between runs, so testing multiple functions returns bogus results.
   - **Note**: Memory usage should be reasonably reliable when passing only a single item in the dict

2. **Problem**: Short benchmarks may not be accurately reported (0 fps). I think it's a psutil bug.
   - **Note**: This should only be a problem for extremely short runs

See [example.py](https://github.com/OpusGang/vs-benchmark/blob/main/example.py) for usage

```
Resolution: 1920x1080

Format: GRAY16
Function     Parameters                                    Threads    TIME      FPS    CPU_USAGE
-----------  ------------------------------------------  ---------  ------  -------  -----------
std boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.67   357.25        43.57
avx boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.39   608.28        48.23
zig boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.82   291.77        42.23
zip boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.32   751.09        26.8
jet boxblur  passes=1, radius=1                                  1    0.15  1636.38        32.53


Format: GRAYS
Function     Parameters                                    Threads    TIME      FPS    CPU_USAGE
-----------  ------------------------------------------  ---------  ------  -------  -----------
std boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    1.6    150.3         53.3
avx boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.84   284.52        51.67
zig boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.95   252.24        36.73
zip boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.21  1155.06        45.27
jet boxblur  passes=1, radius=1                                  1    0.19  1239.09        51.3


Resolution: 3840x2160

Format: GRAY16
Function     Parameters                                    Threads    TIME     FPS    CPU_USAGE
-----------  ------------------------------------------  ---------  ------  ------  -----------
std boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.91   66.26        58
avx boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.57  106.04        50.1
zig boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    1.24   48.28        46.73
zip boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.35  173.51        39.3
jet boxblur  passes=1, radius=1                                  1    0.19  320.6         27.2


Format: GRAYS
Function     Parameters                                    Threads    TIME     FPS    CPU_USAGE
-----------  ------------------------------------------  ---------  ------  ------  -----------
std boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    1.78   33.69        50.87
avx boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    1.17   51.26        59
zig boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    1.45   41.47        44.77
zip boxblur  hpasses=1, vpasses=1, hradius=1, vradius=1          1    0.28  215.31        61.47
jet boxblur  passes=1, radius=1                                  1    0.27  223.93        38.43


Best Functions Comparison (FPS):
Resolution    Format    Best Function    Best Parameters       Best Thread Count    Best FPS
------------  --------  ---------------  ------------------  -------------------  ----------
1920x1080     GRAY16    jet boxblur      passes=1, radius=1                    1     1636.38
1920x1080     GRAYS     jet boxblur      passes=1, radius=1                    1     1239.09
3840x2160     GRAY16    jet boxblur      passes=1, radius=1                    1      320.6
3840x2160     GRAYS     jet boxblur      passes=1, radius=1                    1      223.93
```
