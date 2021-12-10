import psutil
import time
import requests
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import pyshark
import csv
import json
import subprocess as sp
updater = Updater("2133097358:AAFLewQeNHQysJS6sOIJ0L1ZMRuSX-rNTc8", use_context=True)

file = open('./whitelist.csv')
csvreader = csv.reader(file)
whitelist = []
for row in csvreader:
    whitelist.append(row[0])

def log(update: Update, context: CallbackContext):
    i = 0
    while (i<500):
        json_str = sp.check_output("tshark -c 2 -T json".split(' ')).decode('utf-8')
        tshark_pkts = json.loads(json_str)
        pkts_json = [pkt['_source']['layers'] for pkt in tshark_pkts]
        resp = requests.post('http://127.0.0.1:8081/storepkt',json = pkts_json[0])
        print(resp)
        i += 1
    update.message.reply_text("Logging has started...")
    

def modmonitor():
    for proc in psutil.process_iter():
        with proc.oneshot():
            if(proc.pid==0):
                continue
            pname = proc.name()
        if(pname in whitelist):
            continue
        else:
            message =" Detected a new process : " + pname  
            paramperson = {'chat_id':'1158109698','text':message,'parse_mode':'HTML'}
            resp1 = requests.post('https://api.telegram.org/bot2133097358:AAFLewQeNHQysJS6sOIJ0L1ZMRuSX-rNTc8/sendMessage',params=paramperson)


updater.dispatcher.add_handler(CommandHandler('log', log))

modmonitor()
updater.start_polling()