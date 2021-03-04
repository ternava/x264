### 

### specializing x264

Currently, the system of x264 can be specialized regarding 10 configuration options, namely: 
`--mixed-refs`, `--no-mixed-refs`, `--cabac`, `--no-cabac`, `--mbtree`, `--no-mbtree`, `--psy`, `--no-psy`, `--weightb`, `--no-weightb`.

The system can be specialized regarding:
- a single configuration option, e.g., `--cabac`, or 
- a set of them, e.g., `--cabac`, `--psy`, and `-no-weightb`. 

Should be noted that it cannot be specialized by mutually exclusive options, e.g., `--cabac` and `--no-cabac`. 

To specialize x264, there are three steps:
- Receive the sources of x264, which has the posibility to specialize it, e.g., by cloning its branch at your local machine: [details will be given!] 
- [comment]: <>  (`git clone -b x264-rmv https://github.com/ternava/x264.git`)
- In the `removeoption.h` file at the main directory of x264, you need to change the value(s) of the preprocessor directive(s) by which you want to specialize the system. For example, regarding `--cabac`, then you need to set the value of `CABAC_YES` to `0`, as in the following:
```
#ifndef CABAC_NO
#define CABAC_NO 1
#endif
#ifndef CABAC_YES
#define CABAC_YES 0
#endif
```
