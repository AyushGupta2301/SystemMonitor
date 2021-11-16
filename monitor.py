import psutil
import time
import requests
from datetime import datetime


def monitor():
    processes = []

    for proc in psutil.process_iter():
        process = []
        with proc.oneshot():
            if(proc.pid==0):
                continue
            pname = proc.name()
            try:
                pstart = datetime.fromtimestamp(proc.create_time())
            except OSError:
                pstart = datetime.fromtimestamp(psutil.boot_time())

            try:
                pmemory = proc.memory_full_info().uss
            except psutil.AccessDenied:
                pmemory = 0
            pcpu = proc.cpu_percent()
            try:
                ppath = proc.exe()
            except:
                ppath = 'Access Denied'

            pmemory1 = pmemory/(1024*1024)
            pmemory = str(pmemory1) + " MB"

            process.append(proc.pid)
            process.append(pstart)
            process.append(pname)
            process.append(pcpu)
            process.append(pmemory)
            process.append(ppath)
            processes.append(process)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    message = "<b>Report from " + current_time + " => </b>"
    for i in processes:
        if(i[3]>=50):
            message+=" {Process-id : " + str(i[0]) + " :: Name : <b><i>" + i[2] + "</i></b> :: Started : "+ str(i[1])[0:19] + " :: Memory : "+ i[4] +" :: CPU Usage : "+ str(i[3])+"}" 
            paramperson = {'chat_id':'1158109698','text':message,'parse_mode':'HTML'}
            resp = requests.post('https://api.telegram.org/bot2133097358:AAFLewQeNHQysJS6sOIJ0L1ZMRuSX-rNTc8/sendMessage',params=paramperson)
            if(resp.status_code==200):
                print("Report Sent at " + current_time)
            logdata = {'Log Time':current_time,'Process Name':i[2],'Process ID':str(i[0]),'Process Start Time':str(i[1]),'Memory Held':i[4],'CPU Usage':str(i[3]),'Path':i[5]}
            try:
                logresp = requests.post('http://127.0.0.1:8081/store',json=logdata)
            except:
                print("Connection Error With Database, Log recording unsuccessful")
                continue
            if(logresp.status_code==200):
                print("Log Recorded")
            else:
                print("Log recording unsuccessful")
            



iterations = 0
while True:
    monitor()
    iterations += 1
    if(iterations == 60):
        break
    time.sleep(5)
    

