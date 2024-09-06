# vs-benchmark
Moderately extensive tool for benchmarking Vapoursynth functions en masse

Limitations and considerations

- Memory usage is not GC'd between runs, so testing multiple functions returns bogus results 
- Short benchmarks may not accurately be accurately reported (psutil bug maybe)

see example.py for usage

```
Resolution: 3840x2160

  Format: GRAY16
    Format     Function                  Parameters                                         Threads  Avg Time (s) FPS
    ----------------------------------------------------------------------------------------------------------------------
    GRAY16     std boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.187     53.6
    GRAY16     std boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.224     44.7
    GRAY16     std boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.225     44.5
    GRAY16     std boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.266     37.6
    GRAY16     std boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.242     41.4
    GRAY16     std boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.323     31.0
    GRAY16     std boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.289     34.6
    GRAY16     std boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.360     27.8
    GRAY16     std boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.242     41.4
    GRAY16     std boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.291     34.4
    GRAY16     std boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.339     29.5
    GRAY16     std boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.391     25.6
    GRAY16     std boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.291     34.3
    GRAY16     std boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.374     26.7
    GRAY16     std boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.382     26.2
    GRAY16     std boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.464     21.6
    GRAY16     avx boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.285     35.1
    GRAY16     avx boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.121     82.3
    GRAY16     avx boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.123     81.1
    GRAY16     avx boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.126     79.5
    GRAY16     avx boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.219     45.7
    GRAY16     avx boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.127     78.8
    GRAY16     avx boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.132     75.8
    GRAY16     avx boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.126     79.5
    GRAY16     avx boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.124     80.9
    GRAY16     avx boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.127     78.6
    GRAY16     avx boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.123     81.0
    GRAY16     avx boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.129     77.7
    GRAY16     avx boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.214     46.8
    GRAY16     avx boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.164     61.1
    GRAY16     avx boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.162     61.6
    GRAY16     avx boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.151     66.2
    GRAY16     zig boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.239     41.8
    GRAY16     zig boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.239     41.9
    GRAY16     zig boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.248     40.3
    GRAY16     zig boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.239     41.8
    GRAY16     zig boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.233     42.9
    GRAY16     zig boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.226     44.3
    GRAY16     zig boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.232     43.1
    GRAY16     zig boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.226     44.2
    GRAY16     zig boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.265     37.8
    GRAY16     zig boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.259     38.6
    GRAY16     zig boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.263     38.0
    GRAY16     zig boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.261     38.3
    GRAY16     zig boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.239     41.9
    GRAY16     zig boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.245     40.9
    GRAY16     zig boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.240     41.6
    GRAY16     zig boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.259     38.6
    GRAY16     zip boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.078    128.7
    GRAY16     zip boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.233     42.8
    GRAY16     zip boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.274     36.5
    GRAY16     zip boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.083    119.9
    GRAY16     zip boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.277     36.2
    GRAY16     zip boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.261     38.4
    GRAY16     zip boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.247     40.5
    GRAY16     zip boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.251     39.8
    GRAY16     zip boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.324     30.8
    GRAY16     zip boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.312     32.0
    GRAY16     zip boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.321     31.1
    GRAY16     zip boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.299     33.5
    GRAY16     zip boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.306     32.6
    GRAY16     zip boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.318     31.5
    GRAY16     zip boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.314     31.8
    GRAY16     zip boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.323     30.9
    GRAY16     jet boxblur               passes=1, radius=1                                 1               0.054    184.2
    GRAY16     jet boxblur               passes=1, radius=2                                 1               0.054    184.8
    GRAY16     jet boxblur               passes=2, radius=1                                 1               0.072    138.6
    GRAY16     jet boxblur               passes=2, radius=2                                 1               0.082    122.3
    ----------------------------------------------------------------------------------------------------------------------

  Format: GRAYS
    Format     Function                  Parameters                                         Threads  Avg Time (s) FPS
    ----------------------------------------------------------------------------------------------------------------------
    GRAYS      std boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.345     29.0
    GRAYS      std boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.326     30.6
    GRAYS      std boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.319     31.4
    GRAYS      std boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.323     31.0
    GRAYS      std boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.415     24.1
    GRAYS      std boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.417     24.0
    GRAYS      std boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.417     24.0
    GRAYS      std boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.423     23.6
    GRAYS      std boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.416     24.0
    GRAYS      std boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.418     23.9
    GRAYS      std boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.424     23.6
    GRAYS      std boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.413     24.2
    GRAYS      std boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.520     19.2
    GRAYS      std boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.508     19.7
    GRAYS      std boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.513     19.5
    GRAYS      std boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.506     19.8
    GRAYS      avx boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.272     36.8
    GRAYS      avx boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.196     51.0
    GRAYS      avx boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.198     50.4
    GRAYS      avx boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.201     49.8
    GRAYS      avx boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.266     37.7
    GRAYS      avx boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.221     45.3
    GRAYS      avx boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.227     44.0
    GRAYS      avx boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.226     44.3
    GRAYS      avx boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.226     44.2
    GRAYS      avx boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.226     44.3
    GRAYS      avx boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.226     44.3
    GRAYS      avx boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.232     43.2
    GRAYS      avx boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.295     33.9
    GRAYS      avx boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.256     39.0
    GRAYS      avx boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.259     38.6
    GRAYS      avx boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.257     38.8
    GRAYS      zig boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.268     37.4
    GRAYS      zig boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.274     36.5
    GRAYS      zig boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.272     36.7
    GRAYS      zig boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.276     36.3
    GRAYS      zig boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.269     37.2
    GRAYS      zig boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.275     36.4
    GRAYS      zig boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.266     37.6
    GRAYS      zig boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.271     36.9
    GRAYS      zig boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.307     32.5
    GRAYS      zig boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.309     32.4
    GRAYS      zig boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.298     33.5
    GRAYS      zig boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.305     32.7
    GRAYS      zig boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.302     33.1
    GRAYS      zig boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.312     32.1
    GRAYS      zig boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.300     33.3
    GRAYS      zig boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.311     32.1
    GRAYS      zip boxblur               hpasses=1, vpasses=1, hradius=1, vradius=1         1               0.081    123.9
    GRAYS      zip boxblur               hpasses=1, vpasses=1, hradius=1, vradius=2         1               0.291     34.4
    GRAYS      zip boxblur               hpasses=1, vpasses=1, hradius=2, vradius=1         1               0.273     36.7
    GRAYS      zip boxblur               hpasses=1, vpasses=1, hradius=2, vradius=2         1               0.080    125.7
    GRAYS      zip boxblur               hpasses=1, vpasses=2, hradius=1, vradius=1         1               0.272     36.8
    GRAYS      zip boxblur               hpasses=1, vpasses=2, hradius=1, vradius=2         1               0.286     35.0
    GRAYS      zip boxblur               hpasses=1, vpasses=2, hradius=2, vradius=1         1               0.268     37.3
    GRAYS      zip boxblur               hpasses=1, vpasses=2, hradius=2, vradius=2         1               0.279     35.9
    GRAYS      zip boxblur               hpasses=2, vpasses=1, hradius=1, vradius=1         1               0.296     33.8
    GRAYS      zip boxblur               hpasses=2, vpasses=1, hradius=1, vradius=2         1               0.308     32.5
    GRAYS      zip boxblur               hpasses=2, vpasses=1, hradius=2, vradius=1         1               0.291     34.4
    GRAYS      zip boxblur               hpasses=2, vpasses=1, hradius=2, vradius=2         1               0.303     33.0
    GRAYS      zip boxblur               hpasses=2, vpasses=2, hradius=1, vradius=1         1               0.297     33.7
    GRAYS      zip boxblur               hpasses=2, vpasses=2, hradius=1, vradius=2         1               0.306     32.7
    GRAYS      zip boxblur               hpasses=2, vpasses=2, hradius=2, vradius=1         1               0.297     33.6
    GRAYS      zip boxblur               hpasses=2, vpasses=2, hradius=2, vradius=2         1               0.308     32.4
    GRAYS      jet boxblur               passes=1, radius=1                                 1               0.064    155.2
    GRAYS      jet boxblur               passes=1, radius=2                                 1               0.071    141.7
    GRAYS      jet boxblur               passes=2, radius=1                                 1               0.104     96.5
    GRAYS      jet boxblur               passes=2, radius=2                                 1               0.112     89.2
    ----------------------------------------------------------------------------------------------------------------------

Summary of Fastest Results by Resolution and Format:

Resolution: 3840x2160
  Format     Function                  Parameters                                         Threads  Avg Time (s) FPS      Efficiency CPU Usage (%) 
  ------------------------------------------------------------------------------------------------------------------------------------------------
  GRAY16     jet boxblur               passes=1, radius=2                                 1               0.054    184.8       1.00          8.3  
  GRAYS      jet boxblur               passes=1, radius=1                                 1               0.064    155.2       1.00          6.3  
  ------------------------------------------------------------------------------------------------------------------------------------------------
```
