import fileinput
import os
import re
import sys

if(len(sys.argv) != 2 or not os.path.isfile(sys.argv[1])):
    print("Usage: {0} <path to setup.py>".format(os.path.basename(sys.argv[0])))
    sys.exit(1)

pattern = re.compile("\s*version='([0-9.]+)',")
line = ""
maj = "" 
min = "" 
ver = "" 

for line in fileinput.FileInput(sys.argv[1], inplace=1):
    m = pattern.match(line) 
    if m:
        version = m.groups()[0]
        maj, min, rev = version.split('.')
        line = line.replace(version, "{0}.{1}.{2}".format(maj, min, int(rev)+1))

    sys.stdout.write(line)
