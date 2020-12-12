import subprocess
import sys
import glob, os
from datetime import datetime
from pathlib import Path

"""!/_\ This path needs to be updated to your specific path. """
sys.path.append("/home/ternava/Documents/GitHub/x264")

from measures.compilex264 import compilex264

dir_name = "measures/out"
size_data = []

def runx264(x264_exe, input_video, cli_options):
    name = Path(input_video).stem
    for cli_opt in cli_options:
        run_x264 = subprocess.run([x264_exe, 
            cli_opt, 
            "-o", 
            dir_name + "/"+str(cli_opt)+"%s.mkv"% name, 
            input_video])
        run_x264.check_returncode()

def extract_video_metadata(exif_exe, output_video):
    """ From the metadata of output videos are extracted 
    only two: Name and Size """
    video_metadata = subprocess.run([exif_exe, 
        "-s", 
        "-FileName", 
        "-FileSize#", 
        output_video], 
        capture_output=True)

    """ The resulted videos metadata added to a list """
    lst_m = video_metadata.stdout.decode('ascii').split()
    size = int(round(float(lst_m[5])))
    show_metadata = ("The size of " + str(lst_m[2]) + " is: " 
            + str(size) + " bytes")
    size_data.append(show_metadata)
    video_metadata.check_returncode()

#compilex264()

rmv_exe = "./x264"
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
cli_options = ["--cabac", "--no-cabac"] + lst_presets

if os.path.exists(dir_name) and os.path.isdir(dir_name):
    """ First, if existent, the output videos are removed from the folder """
    if len(os.listdir(dir_name)) != 0:
        filelist = [ f for f in os.listdir(dir_name) if f.endswith(".mkv") ]
        for f in filelist:
            os.remove(os.path.join(dir_name, f))
        """ Each specific x264 is used in all input videos """
        for input_video in glob.glob("measures/in/*.mkv"):
            runx264(rmv_exe, input_video, cli_options)
else:
    print("Given directory doesn't exist.")

""" The exiftool for reading the metadata of videos """
exif_exe = "exiftool"
for output_video in glob.glob("measures/out/*.mkv"):
    extract_video_metadata(exif_exe, output_video)

print("\n".join(size_data))
