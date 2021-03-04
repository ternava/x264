### 

### specializing x264

Currently, the system of x264 can be specialized regarding 10 configuration options, namely: 
`--mixed-refs`, `--no-mixed-refs`, `--cabac`, `--no-cabac`, `--mbtree`, `--no-mbtree`, `--psy`, `--no-psy`, `--weightb`, `--no-weightb`.

The system can be specialized regarding:
- a single configuration option, e.g., `--cabac`, or 
- a set of them, e.g., `--cabac`, `--psy`, and `-no-weightb`. 

Should be noted that it cannot be specialized by mutually exclusive options, e.g., using `--cabac` and `--no-cabac` at the same time. 

To specialize x264, there are three steps:
1. Receive the sources of x264 that has the posibility to specialize it, e.g., by cloning this specific branch at your local machine: [details will be given!] 
2. In the `removeoption.h` file at the main directory of x264, you need to change the value(s) of the preprocessor directive(s) by which you want to specialize the system and save it. For instance, to specialize it regarding the configuration option of `--cabac`, you need to set the value of `CABAC_YES` to `0` as in the following:
```
#ifndef CABAC_NO
#define CABAC_NO 1
#endif
#ifndef CABAC_YES
#define CABAC_YES 0
#endif
```
3. Compile the system x264 using `./configure && make`. As a result, the specialized system of x264 will be without the configuration option of `--cabac`. For example, using it to encode a video like here `./x264 --cabac -o <output_video> <input_video>` will show this warning: `./x264: unrecognized option '--cabac'`.





