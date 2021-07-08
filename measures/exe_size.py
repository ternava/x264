import os
import subprocess
import csv
import glob
import fileinput

exe_name = "./x264"

stats_file = "measures/stats_size_gadgets.csv"
header = ['Specialized_sys', 'Binary_size', 'All_gadgets', "ROP_gadgets", "JOP_gadgets", "SYS_gadgets"]

f = open(stats_file, "w")
writer = csv.writer(f)
writer.writerow(header)

def compilex264():
    subprocess.run(["make", "clean"])
    subprocess.run(["./configure"])
    subprocess.run(["make"])

def allgadgets():
    p = subprocess.run(["ROPgadget", "--binary", exe_name], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    nr_of_gadgets = p.stdout.decode('ascii').split()[-1]
    return nr_of_gadgets

def ropgadgets():
    p = subprocess.run(["ROPgadget", "--binary", exe_name, "--nojop", "--nosys"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    nr_of_gadgets = p.stdout.decode('ascii').split()[-1]
    return nr_of_gadgets

def jopgadgets():
    p = subprocess.run(["ROPgadget", "--binary", exe_name, "--norop", "--nosys"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    nr_of_gadgets = p.stdout.decode('ascii').split()[-1]
    return nr_of_gadgets

def sysgadgets():
    p = subprocess.run(["ROPgadget", "--binary", exe_name, "--nojop", "--norop"], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT)
    nr_of_gadgets = p.stdout.decode('ascii').split()[-1]
    return nr_of_gadgets


sample_configurations = []
sample_name = []

for variant in glob.glob("measures/products_10/*.config"):
    lineList = list()
    sample_name.append(str(variant))
    with open(variant) as f:
        for line in f:
            lineList = [line.rstrip('\n') for line in open(variant)]
        sample_configurations.append(lineList)

print(sample_configurations)
print(sample_name)

print("--------------------")

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
    #print(data)
    #close the file
    fin.close()

def change_spec_values(opt):
    # Read in the file
    with open("removeoption.h", 'r') as file:
        filedata = file.read()
    for o in opt:
        # Replace the target string
        filedata = filedata.replace(str(o) + str(" 1") , str(o) + (" 0"))
    # Write the file out again
    with open("removeoption.h", 'w') as file:
        file.write(filedata)

lst_opt = ["MIXED_REFS_YES", "MIXED_REFS_NO", 
        "CABAC_YES", "CABAC_NO", 
        "MBTREE_YES", "MBTREE_NO", 
        "PSY_YES", "PSY_NO",
        "WEIGHTB_YES", "WEIGHTB_NO"]

def change_all_0to1():
    for optb in lst_opt:
        change_values(optb, " 0", " 1")

def calculate_stats(exe_name):
    exe_stats = os.stat(exe_name)
    print(exe_stats)
    exe_size = exe_stats.st_size
    return exe_size

def print_csv(opt):
    exe_size = calculate_stats(exe_name)
    nr_all_gadgets = allgadgets()
    nr_ROP_gadgets = ropgadgets()
    nr_JOP_gadgets = jopgadgets()
    nr_SYS_gadgets = sysgadgets()
    binary_sg = [opt, exe_size, nr_all_gadgets, nr_ROP_gadgets, nr_JOP_gadgets, nr_SYS_gadgets]
    writer.writerow(binary_sg)

def do_operations(opto):
    change_spec_values(opto)
    compilex264()
    print_csv(opto)

# This can be removed if the sample_configuration list contains the [] array
change_all_0to1()
compilex264()
print_csv("BASELINE")

for opt in sample_configurations:
    change_all_0to1()
    print(opt)
    print("-----")
    do_operations(opt)