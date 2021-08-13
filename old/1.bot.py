import os
import telebot

#API_KEY = os.environ['API_KEY']
API_KEY = '1940095882:AAFFnjdLt75e9L6sg_-E59QzFqU3jKCxYNs'

bot=telebot.TeleBot(API_KEY)

###Function

import os
import telebot

API_KEY = os.environ['API_KEY']
bot=telebot.TeleBot(API_KEY)

###Function


@bot.message_handler(commands=['Greetings'])
def greettings(message):
  bot.reply_to(message, 'Jelou, turu!')


def is_youtube(message):
  request = message.text
  print(request)
  print(request[:32])
  if request[:32] == 'https://www.youtube.com/watch?v=':
    print('True')
    return True
  else:
    bot.reply_to(message, 'This video is not a YouTube link. Please supply a a link with the structure https://www.youtube.com/watch?v=.......')
    return False



@bot.message_handler(func=is_youtube)
def is_youtube(message):
  bot.reply_to(message, 'Is you tube!')
  #call the function here


@bot.message_handler(commands=['Docs'])
def doc(message):
  bot.send_message(message.chat.id, 'Your file trasncription')
  doc = open('Test.txt', 'rb')
  bot.send_document(message.chat.id, doc)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

@bot.message_handler(commands=['Greetings'])
def greettings(message):
  bot.reply_to(message, 'Jelou, turu!')

@bot.message_handler(commands=['Greets'])
def greet(message):
  bot.send_message(message.chat.id, 'Jelou, tururu!')
  print('OK')

@bot.message_handler(commands=['Docs'])
def doc(message):
  bot.send_message(message.chat.id, 'Your file transcription')
  doc = open('Test.txt', 'rb')
  bot.send_document(message.chat.id, doc)

#Standard answer for not recognised answer

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()