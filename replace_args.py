import re
import shutil
from tempfile import mkstemp
import sys 

def mk_args(args):
    a_args = args.split(" ")
    argc = len(a_args)

    str_args = f'argc = {argc};\n'
    i = 0
    for a in a_args:
        str_args = str_args + f'argv[{i}] = "{a}"; \n'
        i = i + 1
    return str_args


print(mk_args("x264 --no-cabac --no-mbtree benchs/inputs/original_videos_Animation_480P_Animation_480P-087e.mkv -o o1.mkv"))

# https://stackoverflow.com/a/40843600/13748216
def sed(pattern, replace, source, dest=None, count=0):
    """Reads a source file and writes the destination file.

    In each line, replaces pattern with replace.

    Args:
        pattern (str): pattern to match (can be re.pattern)
        replace (str): replacement str
        source  (str): input filename
        count (int): number of occurrences to replace
        dest (str):   destination filename, if not given, source will be over written.        
    """

    fin = open(source, 'r')
    num_replaced = count

    if dest:
        fout = open(dest, 'w')
    else:
        fd, name = mkstemp()
        fout = open(name, 'w')

    for line in fin:
        out = re.sub(pattern, replace, line)
        
        fout.write(out)

        if out != line:
            num_replaced += 1
        if count and num_replaced > count:
            break
    try:
        fout.writelines(fin.readlines())
    except Exception as E:
        raise E

    fin.close()
    fout.close()

    if not dest:
        shutil.move(name, source) 

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("please give x264 parameters")
        exit
    else:
        x264_cmd =  mk_args(sys.argv[1]) # mk_args("x264 --no-cabac --no-mbtree benchs/inputs/original_videos_Animation_480P_Animation_480P-087e.mkv -o o1.mkv")
        sed("// OVERRIDE_MAIN_ARGUMENTS", x264_cmd, "x264.c.old", dest="x264.c")