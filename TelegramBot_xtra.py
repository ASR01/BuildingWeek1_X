import os
import re
import telebot
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from time import sleep
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

#clear the terminal
#clear = lambda: os.system('cls') # or clear IN LINUX
#clear()

#API_KEY = os.environ['API_KEY']
#API_KEY = os.getenv('API_KEY')

fileTB = open("./API_bot2.txt", "r")
fileYT = open("./API_yt.txt", "r")
#ytAPI = 'AIzaSyBLMVnk_tZFFNCcSTXTdfvjAzAH5tDJ5eQ'
#tbAPI = 'AIzaSyBLMVnk_tZFFNCcSTXTdfvjAzAH5tDJ5eQ'
ytAPI = fileYT.read()
tb_key = fileTB.read()

bot=telebot.TeleBot(tb_key)


### Define Dict to use
######################################################


### Function Youtube API
###############################################################################################
def get_data(dd):
  print('get data')
  
  #rd = result_dict
  md = dd
  print(md['url'])
  youtube = build('youtube', 'v3', developerKey = ytAPI)
  
#  request = youtube.captions().list(part='snippet', videoId = video_id)
#  info2 = request.execute()
  #print(dd['id'])
  request = youtube.videos().list(part='contentDetails, liveStreamingDetails, localizations,player, recordingDetails, snippet, statistics, status', id = dd['id'])
  info = request.execute()
  #print(info)
  vCount = info['items'][0]['statistics']['viewCount']
  likeCount = info['items'][0]['statistics']['likeCount']
  dislikeCount = info['items'][0]['statistics']['dislikeCount']
  favoriteCount = info['items'][0]['statistics']['favoriteCount']
  commentCount = info['items'][0]['statistics']['commentCount']
  title = info['items'][0]['snippet']['title']
  desc= info['items'][0]['snippet']['description']
  tags = info['items'][0]['snippet']['tags']
  length = info['items'][0]['contentDetails']['duration']
  length = length[2:].replace('H',':').replace('M',':').replace('S','')
  licensed = info['items'][0]['contentDetails']['licensedContent']

  #file_title = title
  file_title = re.sub('[\W_]+', '', title)
  #file_title = file_title.replace(' ','_')
  #file_title= file_title.replace('-','_')
  file_title = file_title[:20]
  if licensed == True:
        licensed = 'Yes'
  else:
        licensed = 'No'
  tags = str(tags)

  
  md['valid link'] = True
  md['views'] = vCount
  md['pos']= likeCount
  md['neg']= dislikeCount
  md['comments']= commentCount
  md['fav'] = favoriteCount
  md['length'] = length
  md['description'] = desc
  md['licensed'] = licensed
  md['tags'] = tags
  md['title'] = title
  md['file_title'] = file_title
  
  bot.send_message(md['chatid'], 'Title:\t' + md['title'] + '\n\nViews:\t' + md['views'] + '\n\nLength:\t' + md['length'] + '\n\nPositive Reaction:\t' + md['pos'] + '\n\nNegative Reaction:\t' + md['neg'] + '\n\nComments:\t' + md['comments'])
  bot.send_message(md['chatid'], '\n\nDescription:\t' + md['description'] + '\n\nVideo Licensed:\t' + md['licensed'] + '\n\nTags:\t' + md['tags'] + '\n\nFile Title:\t' + md['file_title'] + '.txt' + '\n\nURL:\t' + md['url'] )
  
  textfile = 'Title:\t' + md['title']
  textfile += '\n\nURL:\t' + md['url']
  textfile += '\n\nViews:\t' + md['views'] + '\n\nLength:\t' + md['length']
  textfile += '\n\nPositive Reaction:\t' + md['pos'] + '\n\nNegative Reaction:\t' + md['neg']
  textfile += '\n\nComments:\t' + md['comments'] + '\n\nNegative Reaction:\t' + md['neg']
  textfile += '\n\nDescription:\t' + md['description'] + '\n\nVideo Licensed:\t' + md['licensed']
  textfile += '\n\nTags:\t' + md['tags'] + '\n\nFile Title:\t' + md['file_title'] + '.txt'
  
  with open('./tr/' + md['file_title'] + '.txt', 'w') as text_file:
      text_file.write(textfile)
      
  #print(md)
  try:
    l = YouTubeTranscriptApi.get_transcript(md['id'])
    #print(len(l), l)
    t = ''
    tt = ''
    x = 0
    while x < len(l):
        temp = l[x]['text'].replace('\n','') + '\n'
        t += temp
        minutes = int(l[x]['start']//60)
        seconds = int(l[x]['start']%60)
        #ts = str(minutes) + ':' + str(seconds)
        ts = str("%d:%02d" % (minutes, seconds))
        t = temp
        tt += ts + '\t-\t' + temp
        x += 1

    
    md['transc'] = t
    md['transc_t'] = tt
    
    #print(md)
    
    textfile = '\n\nTranscription:\n' + ' ' +md['transc_t']
    
    with open('./tr/' + md['file_title'] + '.txt', 'a') as text_file:
      text_file.write(textfile)
    
    bot.send_message(md['chatid'], 'Your file transcription is delivered in the following file.')
    file_addr = './tr/' + md['file_title'] + '.txt'
    doc = open(file_addr, 'rb')
    bot.send_document(md['chatid'], doc)
  except:
    print('error')
    bot.send_message(md['chatid'], 'The requested file has no available transcription or does not exist. \nPlease try another video link.')
       
  
  return md

#### Get Url
###################################################################################################
def get_url(string):
    url = string 
    
    if url[:32] == 'https://www.youtube.com/watch?v=':
          id = url[32:43]
          url = url[:43]
    elif url[:31] == 'http://www.youtube.com/watch?v=':
          id = url[31:42]
          url = url[:42]
    elif url[:16] == 'http://youtu.be/':
          id = url[16:27]
          url = url[:27]
    elif url[:17] == 'https://youtu.be/' :
          id = url[17:28]
          url = url[:28]
    else:
          id = None
    return id
  
#### Check Url
###################################################################################################

def valid_link(url):
  if url[:32] == 'https://www.youtube.com/watch?v=' or url[:31] == 'http://www.youtube.com/watch?v=' or url[:16] == 'http://youtu.be/' or url[:17] == 'https://youtu.be/':
    return True
  else: 
    return False


### Bot functions
#########################################################################################################

@bot.message_handler(commands=['start'])
def start(message):
      print('Interaction')
      bot.reply_to(message, 'Welcome to the transcript extracting bot. \nPlease send a valid youtube address and you will receive a transcript of the spoken audio.')
  
@bot.message_handler(commands=['help'])
def greetings(message):
  print("welcome message")
  bot.reply_to(message, 'Welcome to the YouTube Transcripter.\n\n You have two ways of giving input:\n a) Give us a valid YouTube address.\n b) Type @vid followed by the topic you want and select your video.\n\nIf the video has a transcription we will deliver it to you ASAP.\n\nPlease be reminded that the adresses type bit.ly or youtu.be are not recognised by the system.')
  print("/welcome message")

def youtube(message):
  url = message.text
  print('youtube')
  if valid_link(url) == True:
    return True
  else:
    bot.reply_to(message, 'This address is not a YouTube link. \n\nPlease supply a a link with the structure \nwww.youtube.com/watch?v=.......\n\n If you need help, please type "/help"')
    return False


@bot.message_handler(func=youtube)
def main_action(message):
  print ('func youtube')    
  bot.reply_to(message, 'It is a correct YouTube format address!\nYou will recibe promptly a message with a text file with the transcription in it.')
  md = {
        'valid link' : None,
        'views' : None,
        'pos'   : None,
        'neg'   : None,
        'comments': None,
        'fav' : None,
        'length' : None,
        'description' : '',
        'licensed' : '',
        'tags' : '',
        'title' :None,
        'file_title' : None,
        'id' : None,
        'url' : message.text,
        'transc_t' : None,
        'transc' : None,
        'language' : '',
        'chatid' :message.chat.id
        
        }

@bot.message_handler(commands=['help'])
def greetings(message):
  print("welcome message")
  bot.reply_to(message, 'Welcome to the YouTube Transcripter.\n\n You have two ways of giving input:\n a) Give us a valid YouTube address.\n b) Type @vid followed by the topic you want and select your video.\n\nIf the video has a transcription we will deliver it to you ASAP.\n\nPlease be reminded that the adresses type bit.ly or youtu.be are not recognised by the system.')
  print("/welcome message")



#  md['url']=message.text
#  md['chat']=message.chat.id
  

  md['id'] = get_url(md['url'])
  print(md)
  md = get_data(md)
  #md = get_trans(md)
  
@bot.message_handler(commands=['search'])
def search(message):
  print("search")
  bot.reply_to(message, 'Print' + md['transc'])
  print("/search")

  
  
bot.polling()
