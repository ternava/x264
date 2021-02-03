import os
import subprocess

def compilex264():
    subprocess.run(["./configure"])
    subprocess.run(["make"])

def change_values(opt, o_value, r_value):
    #read input file with options to be remained or removed
    fin = open("removeoption.h", "rt")
    #read all options to string
    data = fin.read()
    #replace the occurrence of 1/0 with the 0/1 for an option
    data = data.replace(str(opt) + str(o_value), str(opt) + str(r_value))
    #close the input file
    fin.close()
    #open the input file with options
    fin = open("removeoption.h", "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

exe_name = "./x264"

def calculate_stats(exe_name):
    exe_stats = os.stat(exe_name)
    print(exe_stats)
    exe_size = exe_stats.st_size
    return exe_size

def print_stats(opt, orgn_size): 
    print(f'Exe size in Bytes is {calculate_stats(exe_name)}')
    print(f'Exe size in MegaBytes is {calculate_stats(exe_name) / (1024 * 1024)}')
    print("Exe size when " + 
        str(opt) + " is removed: " + 
        str(calculate_stats(exe_name)) + " bytes, " + 
        calculate_percentage(orgn_size), 
        file=open(stats_file, "a"))

def calculate_percentage(orgn_size): 
    if((orgn_size - calculate_stats(exe_name)) > 0):
        return str("{:.4%}".format(1 - (calculate_stats(exe_name)/orgn_size))) + " less" 
    elif((orgn_size - calculate_stats(exe_name)) < 0):
        return str("{:.4%}".format(abs(1 - (calculate_stats(exe_name)/orgn_size)))) + " more"
    else:
        return str("{:.4%}".format(1 - (calculate_stats(exe_name)/orgn_size))) 

def do_operations():
    lst_opt = ["MIXED_REFS_YES", "MIXED_REFS_NO", 
            "CABAC_YES", "CABAC_NO", 
            "MBTREE_YES", "MBTREE_NO", 
            "PSY_YES", "PSY_NO",
            "WEIGHTB_YES", "WEIGHTB_NO"]
    
    for opt in lst_opt:
        change_values(opt, " 0", " 1")
        
    compilex264()
    orgnl_exe_size = calculate_stats(exe_name)
    print("The size of the original exe is: " + 
        str(orgnl_exe_size) + " bytes", 
        file=open(stats_file, "a"))

    for opt in lst_opt:
        change_values(opt, " 1", " 0")
        compilex264()
        change_values(opt, " 0", " 1")
        print_stats(opt, orgnl_exe_size)

stats_file = "measures/exesize.txt"

if os.path.exists(stats_file):
    os.remove(stats_file)
    do_operations()
else: 
    do_operations()

    