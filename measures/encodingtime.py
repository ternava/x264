import subprocess
import sys
import glob, os
import time
from pathlib import Path
import csv
import ntpath

"""!/_\ This path needs to be updated to your specific path. """
sys.path.append("/home/xternava/Documents/GitHub/x264")

exe_name = "./x264"

def compilex264():
    subprocess.run(["make", "clean"])
    subprocess.run(["./configure"])
    subprocess.run(["make"])

dir_name = "measures/out"
size_data = []
e_time = []
all = []



###########################################################""""""

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

# Resetting all values from 0 to 1, i.e., to baseline configuration
def change_all_0to1():
    for optb in lst_opt:
        change_values(optb, " 0", " 1")

########################################################################

# List of available presets in x264
lst_presets = ["--preset=%s" % p for p in ("ultrafast",
                                  "superfast",
                                  "veryfast",
                                  "faster",
                                  "fast",
                                  "medium",
                                  "slow",
                                  "slower",
                                  "veryslow",
                                  "placebo") ]
cli_options = [] + lst_presets
#cli_options = ["--preset=superfast"]

# Encoding a video by a specialized system with one preset at e time
def do_encoding(x264_exe, input_video, cli_option):
    name = Path(input_video).stem

    start = time.time()
    run_x264 = subprocess.run([x264_exe, 
        cli_option, 
        "-o", 
        dir_name + "/" + str(cli_option) + "%s.mkv"% name, 
        input_video], 
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    end = time.time()

    run_x264.check_returncode()

    encoded_time = f"{end - start:0.4f}"

    bitrate = run_x264.stdout.decode('ascii').split()[-2]
    fps = run_x264.stdout.decode('ascii').split()[-4]
    #print("Bitrate is: " + bitrate)
    
    return encoded_time, bitrate, fps

def print_csv(sys, spec, spec_file, iv, cli_opt):
    time = do_encoding(exe_name, iv, cli_opt)[0]
    bitrate = do_encoding(exe_name, iv, cli_opt)[1]
    fps = do_encoding(exe_name, iv, cli_opt)[2]
    et = [str(sys), str(spec), str(spec_file), str(cli_opt[9:]), str(iv), time, bitrate, fps]
    writer.writerow(et)

def calc(sys, spec, spec_file):
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        """ First, if existent, the output videos are removed from the folder """
        if len(os.listdir(dir_name)) != 0:
            filelist = [ f for f in os.listdir(dir_name) if f.endswith(".mkv") ]
            for f in filelist:
                os.remove(os.path.join(dir_name, f))
            """ Each specific x264 is used in all input videos """
            for input_video in glob.glob("measures/in/*.mkv"):
                for cli_opt in cli_options: 
                #   if(cli_opt[9:] == spec_file):
                    print_csv(sys, spec, spec_file, input_video, cli_opt)
    else:
        print("Given directory doesn't exist.")

def calc2(sys, spec, spec_file, cli_opt):
    for input_video in glob.glob("measures/in/*.mkv"):
        #for cli_opt in cli_options: 
            #if(cli_opt[9:] == spec_file):
            #    print_csv(sys, spec, spec_file, input_video, cli_opt)
            #if((spec_file == "psyno") & ((cli_opt[9:] == "ultrafast") |(cli_opt[9:] == "fast") )):
        print_csv(sys, spec, spec_file, input_video, cli_opt)



# Add specializied systems
sample_configurations = []
specialized_files = []

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def spec_to_array():
    for variant in glob.glob("measures/products_10/*.config"):
        specialized_files.append(path_leaf(variant[:-7]))
        lineList = list()
        with open(variant) as f:
            for line in f:
                lineList = [line.rstrip('\n') for line in open(variant)]
            sample_configurations.append(lineList)

def do_operations(spec, spec_file):
    for cli_opt in cli_options:
        if(cli_opt[9:] == spec_file):
            change_spec_values(spec)
            compilex264()
            calc2("specialized", spec, spec_file, cli_opt)
    
    if(spec_file == "psyno"):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            calc2("specialized", spec, spec_file, cli_opt)

    # Do nothing for psyyes.config file
    
    if((spec_file == "cabacno") | (spec_file == "weightbno")):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            if((cli_opt[9:] != "ultrafast")):
                calc2("specialized", spec, spec_file, cli_opt)

    if((spec_file == "cabacyes") | (spec_file == "weightbyes")):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            if((cli_opt[9:] == "ultrafast")):
                calc2("specialized", spec, spec_file, cli_opt)

    if(spec_file == "mixedrefsno"):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            if not ((cli_opt[9:] == "ultrafast") 
            | (cli_opt[9:] == "superfast") 
            | (cli_opt[9:] == "veryfast") 
            | (cli_opt[9:] == "faster")):
                calc2("specialized", spec, spec_file, cli_opt)
    
    if(spec_file == "mixedrefsyes"):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            if((cli_opt[9:] == "ultrafast") 
            | (cli_opt[9:] == "superfast") 
            | (cli_opt[9:] == "veryfast") 
            | (cli_opt[9:] == "faster")):
                calc2("specialized", spec, spec_file, cli_opt)

    if(spec_file == "mbtreeno"):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            if not ((cli_opt[9:] == "ultrafast") | (cli_opt[9:] == "superfast")):
                calc2("specialized", spec, spec_file, cli_opt)

    if(spec_file == "mbtreeyes"):
        change_spec_values(spec)
        compilex264()
        for cli_opt in cli_options:
            if((cli_opt[9:] == "ultrafast") 
            | (cli_opt[9:] == "superfast")):
                calc2("specialized", spec, spec_file, cli_opt)

#for i in range(2, 11):

header = ['System', 'Option', "FromFile", 'Preset', 'Video', 'EncodingTime', 'EncodingBitrate', 'FPS']
f = open('measures/stats_encoding18.csv', 'w') # + "0%s.csv"% i, 'w')
writer = csv.writer(f)
writer.writerow(header)

# This can be removed if the sample_configuration list contains the [] array
spec_to_array()
change_all_0to1()
compilex264()
calc("baseline", "BASELINE", "nofile")

for idx, spec in enumerate(sample_configurations):
    for finx, spec_file in enumerate(specialized_files):
        if(idx == finx):
            change_all_0to1()
            print(spec)
            print("-----")
            do_operations(spec, spec_file)
            print(specialized_files)
