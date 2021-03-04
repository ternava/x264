### 

### specializing x264

Currently, the system of x264 can be specialized regarding 10 configuration options, namely: 
`--mixed-refs`, `--no-mixed-refs`, `--cabac`, `--no-cabac`, `--mbtree`, `--no-mbtree`, `--psy`, `--no-psy`, `--weightb`, `--no-weightb`.

The system can be specialized regarding:
- a single configuration option, e.g., `--cabac`, or 
- a set of them, e.g., `--cabac`, `--psy`, and `-no-weightb`. 

Should be noted that it cannot be specialized by mutually exclusive options, e.g., `--cabac` and `--no-cabac`. 

To specialize x264, e.g., regarding `--cabac`, there are three steps:
- Receive the sources of x264 with the posibility to specialize it, e.g., by cloning it at your local machine: 
[//]: # "`git clone -b x264-rmv https://github.com/ternava/x264.git`"
- In the `removeoption.h` file at the main directory of x264, the value of the preprocessor directive 
