import os, re
from collections import Counter

def count_added_loc(added_directive):
    count = Counter()
    for subdir, dirs, files in os.walk(r'../x264'):
            for filename in files:
                filepath = subdir + os.sep + filename
                if filepath.endswith(".c") or filepath.endswith(".h"):
                    with open(os.path.join(os.getcwd(), filepath), 'r') as f: 
                        for line in f:
                            for word in line.split():
                                if re.search(added_directive, line, re.I):
                                    count[word] += 1
    return count

def show_results(count, filePath):
    print("Occurrences of the " + directive + ":")
    print(count.most_common())
    print(count.most_common(), file=open(filePath, "a"))

"""The new added directives need to be added to this list"""
added_directives = ["MIXED_REFS_YES", "MIXED_REFS_NO", 
                "CABAC_YES", "CABAC_NO", 
                "MBTREE_YES", "MBTREE_NO", 
                "PSY_YES", "PSY_NO",
                "WEIGHTB_YES", "WEIGHTB_NO"]

""" Counting the added lines of code in x264
as a result of the added preprocessor directives 
to change the binding time of load-time configuration options
to compile time """

filePath = "measures/addedloc.txt"
   
if os.path.exists(filePath):
    os.remove(filePath)
    for directive in added_directives:
        count = count_added_loc(directive)
        show_results(count, filePath) 
else:
    for directive in added_directives:
        count = count_added_loc(directive)
        show_results(count, filePath)