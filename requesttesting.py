import requests
text = '<b>sampletext</b>' + str(66)
paramperson = {'chat_id':'1158109698','text':text,'parse_mode':'HTML'}
paramgroup = {'chat_id':'-761074619','text':'hello rohil billam!!!'}

r1 = requests.post('https://api.telegram.org/bot2133097358:AAFLewQeNHQysJS6sOIJ0L1ZMRuSX-rNTc8/sendMessage',params=paramperson)

print(r1.json())