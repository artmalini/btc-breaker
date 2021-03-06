import os
import requests
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler

# Token from telegram bot
token = '1133441656:AAG-QbxRVKPqYkCSaR3H0bV9ucc6nJOpHBs'#os.environ["TOKEN"]

# chat_id / group_id = "-302185985"
chat_id = '1238000489'

# port for ngrok http 5000
port = 443


def getHttpsUrl():
    url = "http://localhost:4040/api/tunnels"
    resp = requests.get(url)
    _tmp = None
    if resp.ok:
        data = resp.json()
        
        for tunnel in (data.get("tunnels", [])):
            if "https" in tunnel.get("public_url", ""):
                _tmp = tunnel.get("public_url")
    return _tmp


def sendMessage(text):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(token, chat_id, text)
    #url = "https://api.telegram.org/bot{}/getMe".format(token)
    resp = requests.get(url)
    data =resp.json()
    print (data)

def restart(mymessage):
    print('Tick! The time is: %s' % datetime.now())
    command = 'ngrok http {} > /tmp/ngrok.log &'.format(port)
    os.system(command)
    text = getHttpsUrl()
    time.sleep(1)
    if text:
        sendMessage(mymessage)
    else:
        sendMessage("Please check your logs .. something went wrong..with ngrok.")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(restart, 'interval', hours=6)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print('Err')
        # Not strictly necess