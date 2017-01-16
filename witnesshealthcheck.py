#!/usr/bin/env python3
import telnetlib
import time, datetime
import requests
import json
from piston.steem import Steem

steemnode               = "wss://node.steem.ws" # steem node to connect to for info
witness                 = ""                    # Your witness name
use_telegram            = 1                     # whether or not to use telegram
telegram_token          = ""                    # Create your Telegram bot at @BotFather (https://telegram.me/botfather)
telegram_id             = 007                   # Get your telegram id at @MyTelegramID_bot (https://telegram.me/mytelegramid_bot)
pricefeed_updatetreshold = 0                    # hours of no pricefeed updates before you get a notification
seed_host               = ""                    # hostname/ip for the public seed to monitor
seed_port               = 2001                  # port for the public seed to monitor (steem default = 2001)
seed_timeout_check      = 10                    # seconds before timeout is called on telnet public seed operation.

def telegram(method, params=None):
    url = "https://api.telegram.org/bot"+telegram_token+"/"
    params = params
    r = requests.get(url+method, params = params).json()
    return r

steem = Steem(node=steemnode)
info = steem.info()
try:
        bh = steem.info()["head_block_number"]
        print("Connected. Current block height is " + str(bh))
except:
        print("Connection error.")
        quit()

if use_telegram == 1:
        try:
                print("Connecting to Telegram")
                test = telegram("getMe")
        except:
                print("Telegram connection error")
                quit()

#get steem witness info
my_info = steem.rpc.get_witness_by_account(witness)
#last sbd price feed update
lastupdate = time.mktime(datetime.datetime.strptime(my_info['last_sbd_exchange_update'], '%Y-%m-%dT%H:%M:%S').timetuple())
#current timestamp
sinceepochalt = time.mktime(time.gmtime())
#difference in hours (seconds / 3600)
diff = int(sinceepochalt - lastupdate) / 3600

# notify if pricefeed is to old
if diff > pricefeed_updatetreshold:
        tel_msg = "Check your pricefeed on Steemit! \n\nYour last pricefeed update was *"+("{0:.2f}".format(diff))+" hours* ago..."
        print(tel_msg)
        tel_payload = {"chat_id":telegram_id, "text":tel_msg,  "parse_mode": "Markdown"}
        m = telegram("sendMessage", tel_payload)

# check for seednode timeout.
try:
        tn = telnetlib.Telnet(seed_host, seed_port,seed_timeout_check)
        print(tn.read_all())
except Exception as e:
        tel_msg = "Check your seednode at *"+seed_host+"*.\n\n_"+str(e)+"_"
        print(tel_msg)
        tel_payload = {"chat_id":telegram_id, "text":tel_msg, "parse_mode": "Markdown"}
        m = telegram("sendMessage", tel_payload)
