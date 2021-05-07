import subprocess
import sys, os

from options import all_options, all_s_options

stats_file = "measures/exesize_2-200.csv"
exe_path = "./x264"

i_options = all_s_options

def calculate_stats(exe_path):
    exe_stats = os.stat(exe_path)
    print(exe_stats)
    exe_size = exe_stats.st_size
    return exe_size

def print_stats(opt): 
    print(f'Exe size in Bytes is {calculate_stats(exe_path)}')
    print(f'Exe size in MegaBytes is {calculate_stats(exe_path) / (1024 * 1024)}')
    print("Exe size when " + 
        str(opt) + " is: " + 
        str(calculate_stats(exe_path)) + " bytes, ", 
        file=open(stats_file, "a"))

def ccompilex264(compile_time_opt):
    subprocess.run(["make", "clean"])
    subprocess.run(["./configure"] + compile_time_opt)
    subprocess.run(["make"])
    
def compilex264(compile_time_opt):
    subprocess.run(["./configure"] + compile_time_opt)
    subprocess.run(["make"])

def do_operations():
    for o in all_s_options:
        ccompilex264(o)
        print_stats(o)
        for opt in all_options:
            compilex264(opt)
            print_stats(opt)
        compilex264(o)
        print_stats(o)


if os.path.exists(stats_file):
    os.remove(stats_file)
    do_operations()
else: 
    do_operations()