import os
import subprocess

exe_name = "./x264"
size_data = []

def compilex264():
    subprocess.run(["./configure"])
    subprocess.run(["make"])

def ropgadget():
    p = subprocess.run(["ROPgadget", "--binary", exe_name], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    print(p)
    nr_of_gadgets = p.stdout.decode('ascii').split()[-1]
    return nr_of_gadgets


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

def calculate_percentage(org_nr, res_nr): 
    if((org_nr - res_nr) > 0):
        return str("{:.4%}".format(1 - (res_nr/org_nr))) + " less" 
    elif((org_nr - res_nr) < 0):
        return str("{:.4%}".format(abs(1 - (res_nr/org_nr)))) + " more"
    else:
        return str("{:.4%}".format(1 - (res_nr/org_nr))) 

def print_nr_gadgets(opt, nr_of_gardgets_01, nr_of_gardgets_02): 
    print("The unique number of found gadgets when " +
        str(opt) + " is removed: " +
        str(nr_of_gardgets_02) + ". Or, " + 
        calculate_percentage(int(nr_of_gardgets_01), int(nr_of_gardgets_02)), 
                            file=open(stats_file, "a"))

def do_operations():
    lst_opt = ["MIXED_REFS_YES", "MIXED_REFS_NO", 
            "CABAC_YES", "CABAC_NO", 
            "MBTREE_YES", "MBTREE_NO", 
            "PSY_YES", "PSY_NO",
            "WEIGHTB_YES", "WEIGHTB_NO"]
    
    for opt in lst_opt:
        change_values(opt, " 0", " 1")
        
    compilex264()
    nr_of_gardgets_01 = ropgadget()
    print("The original unique number of found gadgets is: " +
        str(nr_of_gardgets_01), file=open(stats_file, "a"))

    for opt in lst_opt:
        change_values(opt, " 1", " 0")
        compilex264()
        nr_of_gardgets_02 = ropgadget()
        change_values(opt, " 0", " 1")
        print_nr_gadgets(opt, nr_of_gardgets_01, nr_of_gardgets_02)

stats_file = "measures/gadgetsnr.txt"

if os.path.exists(stats_file):
    os.remove(stats_file)
    do_operations()
else: 
    do_operations()