# vs-benchmark
Moderately extensive tool for benchmarking Vapoursynth functions en masse

See [example.py](https://github.com/OpusGang/vs-benchmark/blob/main/example.py) for usage

```
Progress: 100%|██████████████████████████████| 24/24 [07:53<00:00, 19.73s/test, Function: zip boxblur, Params: {}, Pass: 3]

Resolution: 1920x1080

Format: GRAY16
Function     Params    Time [min, max]    FPS [min, max]             Relative
-----------  --------  -----------------  -----------------------  ----------
std boxblur  {}        6.32 [6.15, 6.51]  158.33 [153.53, 162.50]        0.76
zip boxblur  {}        4.80 [4.79, 4.81]  208.25 [208.03, 208.65]        1

Format: GRAYS
Function     Params    Time [min, max]       FPS [min, max]             Relative
-----------  --------  --------------------  -----------------------  ----------
std boxblur  {}        12.27 [12.22, 12.34]  81.53 [81.06, 81.83]           0.43
zip boxblur  {}        5.23 [5.17, 5.35]     191.14 [186.81, 193.42]        1


Resolution: 3840x2160

Format: GRAY16
Function     Params    Time [min, max]       FPS [min, max]          Relative
-----------  --------  --------------------  --------------------  ----------
std boxblur  {}        26.42 [26.05, 26.61]  37.85 [37.57, 38.39]         0.9
zip boxblur  {}        23.76 [23.64, 23.88]  42.08 [41.87, 42.30]         1

Format: GRAYS
Function     Params    Time [min, max]       FPS [min, max]          Relative
-----------  --------  --------------------  --------------------  ----------
std boxblur  {}        50.44 [49.87, 50.88]  19.83 [19.65, 20.05]        0.57
zip boxblur  {}        28.61 [28.60, 28.63]  34.96 [34.93, 34.97]        1


Best Functions Comparison (FPS):
Resolution    Format    Best Function    Best Parameters      Best FPS
------------  --------  ---------------  -----------------  ----------
1920x1080     GRAY16    zip boxblur      {}                     208.25
1920x1080     GRAYS     zip boxblur      {}                     191.14
3840x2160     GRAY16    zip boxblur      {}                      42.08
3840x2160     GRAYS     zip boxblur      {}                      34.96
```
