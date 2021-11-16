import psutil
import os
processes = []
for i in psutil.process_iter():
    processes.append(i)

scripts = []
paths = []
for pid in processes:
    try:
        scripts.append(pid.cmdline()[1])
        print(pid.exe())
    except:
        pass

for script in scripts:
    paths.append(os.path.abspath(script))

