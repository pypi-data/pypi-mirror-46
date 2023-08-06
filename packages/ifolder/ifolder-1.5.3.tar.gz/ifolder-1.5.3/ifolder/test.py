import os, sys

rel_paths = ['TEST.pdf', 'icon/.DS_Store', 'icon/log.txt', 'icon/read.py', 'icon/F1/.DS_Store', 'icon/F1/456.pdf', 'IBM/.DS_Store', 'IBM/SPSS/.DS_Store', 'IBM/SPSS/Statistics/.DS_Store', 'IBM/SPSS/Statistics/23/statistics.jnl']


spli = splitall('/Users/vt/Desktop/TEST/TEST.pdf')

path_set = set()
for p in rel_paths:
    path_set.add(splitall(p)[0])



print(path_set)

    # files = [
    # '/Users/vt/Desktop/TEST/TEST.pdf',
    # '/Users/vt/Desktop/TEST/icon',
    # '/Users/vt/Desktop/TEST/IBM', 
    # ]