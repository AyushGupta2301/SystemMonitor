import requests
text = '<b>sampletext</b>' + str(66)
paramperson = {'chat_id':'<>','text':text,'parse_mode':'HTML'}
paramgroup = {'chat_id':'<>','text':'hello rohil billam!!!'}

r1 = requests.post('https://api.telegram.org/bot<>/sendMessage',params=paramperson)
# Removed ID and token for security reasons

print(r1.json())