import psutil
import csv

processes = []
for proc in psutil.process_iter():
    process = []
    with proc.oneshot():
        if(proc.pid==0):
            continue
        pname = proc.name()
        process.append(pname)
        processes.append(process)

filename = 'whitelist.csv'
with open(filename, 'a') as file:
    for row in processes:
        for x in row:
            file.write(str(x))
            file.write('\n')