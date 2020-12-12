import subprocess
import sys

def compilex264():
    subprocess.run(["./configure"])
    subprocess.run(["make"])