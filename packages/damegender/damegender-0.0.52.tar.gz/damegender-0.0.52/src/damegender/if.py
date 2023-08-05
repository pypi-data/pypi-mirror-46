import os

cmd = 'grep -i Alicia files/names/nam_dict.txt > files/grep.tmp'
print(cmd)
print(os.system(cmd))
results = [i for i in open('files/grep.tmp','r').readlines()]
for row in results:
    print(row[1].title())
#    print(datasetname)
