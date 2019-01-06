import fileinput
import re
import sys

pattern = re.compile("\s*version='([0-9.]+)',")
line = ""
maj = "" 
min = "" 
ver = "" 

for line in fileinput.FileInput("setup.py", inplace=1):
    m = pattern.match(line) 
    if m:
        version = m.groups()[0]
        maj, min, rev = version.split('.')
        line = line.replace(version, "{0}.{1}.{2}".format(maj, min, int(rev)+1))

    sys.stdout.write(line)
