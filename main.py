# ASIC bot

import config
import btc
import requests
import json
import telebot

from flask import Flask, request, jsonify
from flask_sslify import SSLify
#from telebot import apihelper
#apihelper.proxy = {'http':'http://10.10.1.10:3128'}

server = Flask(__name__)
ssl = SSLify(server)
URL = 'https://api.telegram.org/bot%s/' % config.token
bot = telebot.TeleBot(config.token)

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

#1 pulling
def get_updates():
    r = requests.get(URL + 'getUpdates')
    write_json(r.json())
    return r.json()

def send_message_to_bot(chat_id, text='bla-bla'):
    answer = {'chat_id' : chat_id, 'text' : text}
    r = requests.post(URL + 'sendMessage', json=answer)
    return r.json()

def main():
    r = requests.get(URL + 'getMe')
    res = write_json(r.json(), 'conf.json')
    r = get_updates()
    chat_id = r['result'][-1]['message']['id']
    print (chat_id)
    send_message_to_bot(chat_id, "" )
    command = r['message']['text']
    send_message_to_bot (chat_id, 'ты сказал ' + command + '?')
    return res + chat_id + "btc price=%s" % btc.get_price("BTC")

@server.route('/')
def index():
    #return main()
    return '<h1>I can make bots!</h1>'+ btc.get_miners_info()+btc.get_wallets_info()

@bot.message_handler(commands=['register'])
def start(message):
    sent = bot.send_message( message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(sent, hello)

def hello(message):
    bot.send_message( message.chat.id, 'привет %s' % message.text )

#@bot.message_handler(commands=['wallets','miners','manage'])

@bot.message_handler(commands=['wallets'])
def w(message):
    bot.send_message(message.chat.id, btc.get_wallets_info())

@bot.message_handler(commands=['miners'])
def m(message):
    bot.send_message(message.chat.id, btc.get_miners_info())

@bot.message_handler(commands=['state'])
def m(message):
    bot.send_message(message.chat.id, btc.get_state_info())

#    elif message.text=='/manage':
#        sent=bot.send_message(message.chat.id, 'пока не реализовано')
#    else:
#        sent=bot.send_message(message.chat.id, 'Не понимаю и не могу с этим ничего сделать(')
#    bot.register_next_step_handler(sent, hello)

#@server.route('/')
#def webhook():
#    bot.remove_webhook()
#    bot.polling(non_stop=True)
#    return "polling(non_stop=True)"
    #bot.set_webhook(url=config.https_url)
    #return "web hook setted to " + config.https_url

#@server.route('/', methods=['POST', 'GET'])
#def index():
#    if request.method == 'POST':
#        r = request.get_json()
#        #write_json(r)
#        chat_id = r['message']['chat']['id']
#        command = r['message']['text']
#        send_message_to_bot (chat_id, 'ты сказал ' + command + '?')
#        return jsonify(r)
#    elif request.method == 'GET':
#    #wh = URL + 'setWebhook?url=' + config.https_url
#        return jsonify('<h1>tihon *run* bot on Flask!</h1>')
#    return "<h1>tihon's bot welcomes you !</h1>"


if __name__ == '__main__':
    server.run()

bot.polling() #(non_stop=True)
