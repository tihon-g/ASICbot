const tel_bot = require('node-telegram-bot-api')

const TOKEN =  '519650252:AAGJAcS2ElbbGJfdxCJkvqb3k49ZGvf828o'

const bot = new tel_bot(TOKEN, {polling: true})

bot.on('message', msg => {bot.sendMessage(msg.chat.id, 'Hello from HEROKU, bot says: "Hi, ${msg.from.first_name}"')})
