import subprocess
import sys
import glob, os
os.chdir(".")

""" The original exe of x264 and the one with different removed options. 
!/_\ Testing only the --trellis option.
!/_\ It can run only locally. """
master_exe = "exe/x264"
rmv_exe = "/home/ternava/Documents/GitHub/x264/x264"

""" The exiftool for reading the metadata of videos """
exif_exe = "exiftool"

# master_data = open("out/master_output.txt", "wb")
# rmv_data = open("out/rmv_output.txt", "wb")
diff_data = open("out/diff_data.txt", "w")

lst_master = []
lst_rmv = []
diff_percent = []

output_master_videos = ["out/out01.mkv", "out/out03.mkv", "out/out04.mkv", "out/out05.mkv"]
output_rmv_videos = ["out/rout01.mkv", "out/rout03.mkv", "out/rout04.mkv", "out/rout05.mkv"]

i = 0
for input_video in glob.glob("in/*.mkv"):
    """ Each specific x264 is used in all four input videos """
    master_run = subprocess.run([master_exe, 
        "--preset=superfast", 
        "-o", 
        output_master_videos[i], 
        input_video])
    rmv_run = subprocess.run([rmv_exe,
        "--preset=superfast",
        "-o", 
        output_rmv_videos[i], 
        input_video])
    
    """ From the metadata of output videos are extracted only two: Name and Size """
    master_result = subprocess.run([exif_exe, 
        "-s", 
        "-FileName", 
        "-FileSize#", 
        output_master_videos[i]], 
        capture_output=True)
    rmv_result = subprocess.run([exif_exe, 
        "-s", 
        "-FileName", 
        "-FileSize#", 
        output_rmv_videos[i]], 
        capture_output = True)
    
    i = i + 1
    
    # master_data.write(master_result.stdout)
    # rmv_data.write(rmv_result.stdout)

    """ The resulted videos metadata added to a list """
    lst_m = master_result.stdout.decode('ascii').split()
    lst_r = rmv_result.stdout.decode('ascii').split()
    lst_master.append(lst_m)
    lst_rmv.append(lst_r)

    """ Calculated the difference on the size of original and new videos, in percentage """
    diff = int(round((float(lst_r[5])/float(lst_m[5]))*100))
    #diff_percent.append(diff)
    result = ("The size difference of " + 
        str(lst_r[2]) + " and " + 
        str(lst_m[2]) + " is: " + 
        str(diff) + "%")
    diff_percent.append(result)
    diff_data.write(result + "\n")

    master_run.check_returncode()
    rmv_run.check_returncode()
    master_result.check_returncode()
    rmv_result.check_returncode()

# master_data.close()
# rmv_data.close()
diff_data.close()

print("\n".join(diff_percent))
