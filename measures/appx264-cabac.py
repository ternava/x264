import subprocess
import sys
import glob, os
import time
from pathlib import Path
import csv

"""!/_\ This path needs to be updated to your specific path. """
sys.path.append("/home/xternava/Documents/GitHub/x264")

#from measures.compilex264 import compilex264

exe_name = "./x264"

def compilex264():
    subprocess.run(["make", "clean"])
    subprocess.run(["./configure"])
    subprocess.run(["make"])

dir_name = "measures/out"
size_data = []
e_time = []
all = []

header = ['Specialized_sys', 'Option', 'Video', 'Encoding_time']
f = open('measures/stats_encoding_time.csv', 'w')
writer = csv.writer(f)
writer.writerow(header)

###########################################################""""""
sample_configurations = []

for variant in glob.glob("measures/products_10/*.config"):
    lineList = list()
    with open(variant) as f:
        for line in f:
            lineList = [line.rstrip('\n') for line in open(variant)]
        sample_configurations.append(lineList)

# print(sample_configurations)

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

########################################################################



def runx264(x264_exe, input_video, cli_options):
    name = Path(input_video).stem

    for cli_opt in cli_options:

        #start = time.perf_counter()
        start = time.time()

        run_x264 = subprocess.run([x264_exe, 
            cli_opt, 
            "-o", 
            dir_name + "/"+str(cli_opt)+"%s.mkv"% name, 
            input_video, 
            ]) 
        
        #end = time.perf_counter()
        end = time.time()
        #encoded_time = "Encoded time for " + str(cli_opt) + "%s.mkv"% name + f" is {end - start:0.4f} seconds"
        encoded_time = ["non", str(cli_opt), "%s.mkv"% name, f"{end - start:0.4f}"]
        e_time.append(encoded_time)
        all.append(encoded_time) # for csv
        print(encoded_time)

        writer.writerow(encoded_time)
        run_x264.check_returncode()


def calculate_encoding_time(x264_exe, input_video, cli_option):
    name = Path(input_video).stem
    start = time.time()
    run_x264 = subprocess.run([x264_exe, 
        cli_option, 
        "-o", 
        dir_name + "/"+str(cli_option)+"%s.mkv"% name, 
        input_video])
    run_x264.check_returncode()
    end = time.time()
    #encoded_time = [str(specialization), str(cli_option), "%s.mkv"% name, f"{end - start:0.4f}"]
    encoded_time = f"{end - start:0.4f}"
    return encoded_time


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



def print_csv(spec, iv, cli_opt):
    encoding_time = calculate_encoding_time(exe_name, iv, cli_opt)
    et = [str(spec), str(cli_opt), str(iv), encoding_time]
    writer.writerow(et)

def calc(spec):
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        """ First, if existent, the output videos are removed from the folder """
        if len(os.listdir(dir_name)) != 0:
            filelist = [ f for f in os.listdir(dir_name) if f.endswith(".mkv") ]
            for f in filelist:
                os.remove(os.path.join(dir_name, f))
            """ Each specific x264 is used in all input videos """
            for input_video in glob.glob("measures/in/*.mkv"):
                #runx264(rmv_exe, input_video, cli_options)
                for cli_opt in cli_options: 
                    print_csv(spec, input_video, cli_opt)
    else:
        print("Given directory doesn't exist.")



def do_operations(spec):
    change_spec_values(spec)
    compilex264()
    calc(spec)

# This can be removed if the sample_configuration list contains the [] array
#change_all_0to1()
#compilex264()
#print_csv("BASELINE")

for spec in sample_configurations:
    change_all_0to1()
    print(spec)
    print("-----")
    do_operations(spec)






















#def extract_video_metadata(exif_exe, output_video):
    """ From the metadata of output videos are extracted 
    only two: Name and Size """
 #   video_metadata = subprocess.run([exif_exe, 
 #       "-s", 
 #       "-FileName", 
 #       "-FileSize#", 
 #       output_video], 
 #       capture_output=True)

    """ The resulted videos metadata added to a list """
 #   lst_m = video_metadata.stdout.decode('ascii').split()
 #   size = int(round(float(lst_m[5])))
 #   show_metadata = ("The size of " + str(lst_m[2]) + " is: " 
 #           + str(size) + " bytes")
 #   size_data.append(show_metadata)
 #   all.append(size) # for csv
 #   video_metadata.check_returncode()

""" 
    lst_opt = ["MIXED_REFS_YES", "MIXED_REFS_NO", 
                "CABAC_YES", "CABAC_NO", 
                "MBTREE_YES", "MBTREE_NO", 
                "PSY_YES", "PSY_NO",
                "WEIGHTB_YES", "WEIGHTB_NO"]
    
    for opt in lst_opt:
        change_values(opt, " 0", " 1") """



""" The exiftool for reading the metadata of videos """
""" exif_exe = "exiftool"


filePath = "measures/videosize.cvs"


if os.path.exists(filePath):
    os.remove(filePath)
    for output_video in glob.glob("measures/out/*.mkv"):
        extract_video_metadata(exif_exe, output_video)
    print("\n".join(size_data) + "\n" + "\n".join(e_time), file=open(filePath, "a"))
    print("\n".join(size_data))
else:
    for output_video in glob.glob("measures/out/*.mkv"):
        extract_video_metadata(exif_exe, output_video)
    print("\n".join(size_data) + "\n" + "\n".join(e_time), file=open(filePath, "a"))
    print("\n".join(size_data)) """
