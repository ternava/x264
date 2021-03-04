### 

### specializing x264

Currently, the system of x264 can be specialized regarding 10 configuration options, namely: 
```
--mixed-refs, --no-mixed-refs
--cabac, --no-cabac
--mbtree, --no-mbtree
--psy, --no-psy
--weightb, --no-weightb
```

There are two possible specialization scenarions:
- using a single configuration option, e.g., `--cabac`, or 
- using a set of configuration options, e.g., `--cabac`, `--psy`, and `-no-weightb`. 

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


### measurements

There are 4 Python scripts that can help to measure 5 things in the original or specialized system of x264. 

##### Counting the number of added lines of code (LoC): 
The script `measures/addedloc.py` is used to count the number of LoC that we added tp delimit each of the 10 configuration options. To use it, in the original system of x264, you simply need to run the script using `python3 measures/addedloc.py` and it will generate a file named `addedloc.txt` with information about the added LoC.

##### Measuring the binary size
The script `measures/exe_size.py` is used to measure the binary size of the original and specialized systems of x264 by any of the 10 configuration options. 
To use it, you simply need to run the script using `python3 measures/exe_size.py` and it will generate a file named `èxesize.txt` with information about the binary size in bytes of each executable and their differences in percentage from the original system.

##### Measuring the number of gadgets
The script `measures/exe_gadgets.py` is used to count the number of gadgets in the original and ten specialized systems of x264. To use it, you simply need to run the sricpt using `python3 measures/exe_gadgets.py` and it will generate a file named `gadgetsnr.txt` with information about the number of found gadgets in the original and specialized systems, including their difference to the original system in percentage. 

##### Checking for soundness and measuring the encoding time
The script `measures/appx264-cabac.py` is used for two reasons, in the original and ten specialized systems:
  - to measure the video size in bytes after its encoding, which measure we use to check the soundness of a system
  - to measure the encoding time of a video, measures in seconds.

To use it, you simply need to run the script using `python3 measures/appx264-cabac.py` and it will generate a file named `videosize.txt` with information about the encoded video size and its used encoded time for ten presets in x264 (see http://www.chaneru.com/Roku/HLS/X264_Settings.htm#preset).







