#!/bin/sh

# parameters of the script
# (1) input sensitivity 
ivideo="benchs/inputs/original_videos_LyricVideo_360P_LyricVideo_360P-5e87.mkv" # "benchs/inputs/original_videos_Animation_480P_Animation_480P-087e.mkv"
# (2) options sensitivity 
x264_opts="--no-cabac --no-mbtree" # TODO: should not be empty

x264_args="x264 $x264_opts $ivideo -o o1.mkv" 

# first, let's breath command line arguments for x264 
# the idea is to fix argc and argv right in the main function of x264.c, see x264_replace_args.py for more details
# not an idea solution, but I can't make it work properly directly within gcov 
python x264_replace_args.py "$x264_args"

make 
./x264 $x264_args
gcov -o ./x264 
lcov --directory . -c --output-file x264_coverage.info
genhtml -o x264-coverage_report/ -t "x264 coverage" x264_coverage.info
