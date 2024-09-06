# vs-benchmark
Moderately extensive tool for benchmarking Vapoursynth functions en masse

Limitations and considerations
    - Memory usage is not GC'd between runs, so testing multiple functions returns bogus results 
    - Short benchmarks may not accurately be accurately reported (psutil bug maybe)

see example.py for usage
