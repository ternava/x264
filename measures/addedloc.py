import os, re, csv
import os

from collections import Counter

def count_added_loc(added_directive):
    count = Counter()
    count_files = []
    files_in_project =  0
    for subdir, dirs, files in os.walk(r'../x264'):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".c") or filepath.endswith(".h"):
                    files_in_project  += 1 
                    with open(os.path.join(os.getcwd(), filepath), 'r') as f: 
                        for line in f:
                            for word in line.split():
                                if re.search(added_directive, line, re.I):
                                    count[word] += 1
                                    count_files.append(filepath)

    print("Overall files in the project are: " + files_in_project)
    return count, count_files


"""The new added directives need to be added to this list"""
added_directives = [["MIXED_REFS_YES", "--mixed-refs"], 
                ["MIXED_REFS_NO", "--no-mixed-refs"], 
                ["CABAC_YES", "--cabac"], 
                ["CABAC_NO", "--no-cabac"], 
                ["MBTREE_YES", "--mbtree"], 
                ["MBTREE_NO", "--no-mbtree"], 
                ["PSY_YES", "--psy"], 
                ["PSY_NO", "--no-psy"],
                ["WEIGHTB_YES", "--weightb"], 
                ["WEIGHTB_NO", "--no-weightb"]]

""" Counting the added lines of code in x264
as a result of the added preprocessor directives 
to change the binding time of load-time configuration options
to compile time """

filePath = "measures/stats_addedloc.csv"
header = ['Option', 'Word', 'Directive', 'WCount', 'InFiles', 'FCount']
f = open(filePath, 'w')
writer = csv.writer(f)
writer.writerow(header)

def show_results(option, count, filePath, files, nrfiles):
    #print("Occurrences of the " + directive + ":")
    #print(count.most_common())
    #print(count.most_common(), file=open(filePath, "a"))
    stat = [str(option), str(directive), str(count.most_common()[0][0]), str(count.most_common()[0][1]), str(files), str(nrfiles)]
    writer.writerow(stat)


""" if os.path.exists(filePath):
    os.remove(filePath)
    for directive in added_directives:
        count = count_added_loc(directive)
        show_results(count, filePath) 
else:
    for directive in added_directives:
        count = count_added_loc(directive)
        show_results(count, filePath) """

for directive in added_directives:
        count = count_added_loc(directive[0])[0]
        files = list(set(count_added_loc(directive[0])[1]))
        option = directive[1]
        show_results(option, count, filePath, files, len(files))