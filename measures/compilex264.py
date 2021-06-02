import subprocess
import sys, os
import time

from options import all_options, all_s_options

stats_file01 = "measures/exesize_1.csv"
stats_file02 = "measures/exesize_2.csv"
exe_path = "./x264"

i_options = all_s_options
e_time = []

def calculate_stats(exe_path):
    exe_stats = os.stat(exe_path)
    print(exe_stats)
    exe_size = exe_stats.st_size
    return exe_size

def print_stats01(opt, time): 
    print(f'Exe size in Bytes is {calculate_stats(exe_path)}')
    print(f'Exe size in MegaBytes is {calculate_stats(exe_path) / (1024 * 1024)}')
    print("Exe size when " + 
        str(opt) + " is: " + 
        str(calculate_stats(exe_path)) + " bytes, " + time, 
        file=open(stats_file01, "a"))

def print_stats02(opt, time): 
    print(f'Exe size in Bytes is {calculate_stats(exe_path)}')
    print(f'Exe size in MegaBytes is {calculate_stats(exe_path) / (1024 * 1024)}')
    print("Exe size when " + 
        str(opt) + " is: " + 
        str(calculate_stats(exe_path)) + " bytes, " + time, 
        file=open(stats_file02, "a"))

def ccompilex264(compile_time_opt):
    start = time.time()
    subprocess.run(["make", "clean"])
    subprocess.run(["./configure"] + compile_time_opt)
    subprocess.run(["make"])
    end = time.time()
    encoded_time = "Encoded time for " + str(compile_time_opt) + f"is {end - start:0.4f} seconds"
    e_time.append(encoded_time)
    #print(encoded_time)
    return encoded_time
    
def compilex264(compile_time_opt):
    start = time.time()
    subprocess.run(["./configure"] + compile_time_opt)
    subprocess.run(["make"])
    end = time.time()
    encoded_time = "Encoded time for " + str(compile_time_opt) + f" is {end - start:0.4f} seconds"
    e_time.append(encoded_time)
    #print(encoded_time)
    return encoded_time

def do_operations():
    for o in all_s_options:
        tm01 = ccompilex264(o)
        print_stats01(o,tm01)
        for opt in all_options:
            tm02 = compilex264(opt)
            print_stats02(opt, tm02)
        tm03 = compilex264(o)
        print_stats01(o, tm03)


if os.path.exists(stats_file01):
    os.remove(stats_file01)
    if os.path.exists(stats_file02):
        os.remove(stats_file02)
    do_operations()
else: 
    do_operations()