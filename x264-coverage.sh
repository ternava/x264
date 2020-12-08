#!/bin/sh
ivideo="benchs/inputs/original_videos_Animation_480P_Animation_480P-087e.mkv"
make 
./x264 --preset veryslow $ivideo -o output.mkv
gcov -o ./x264 './x264 --preset veryslow $ivideo -o output.mkv'
lcov --directory . -c --output-file x264_coverage.info
genhtml -o x264-coverage_report/ -t "x264 coverage" x264_coverage.info


