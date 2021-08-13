import os
import re
import telebot
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from time import sleep
import markdown
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

#clear the terminal
#clear = lambda: os.system('cls') # or clear IN LINUX
#clear()

#API_KEY = os.environ['API_KEY']
#API_KEY = os.getenv('API_KEY')

fileAPI = open("./BW1/API.txt", "r")
ytAPI = 'AIzaSyBLMVnk_tZFFNCcSTXTdfvjAzAH5tDJ5eQ'
API_KEY = fileAPI.read()
bot=telebot.TeleBot(API_KEY)


### Define Dict to use
######################################################


### Function Youttube API
###############################################################################################
def get_data(dd):
  
  #rd = result_dict
  md = dd
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
  
  with open('./BW1/tr/' + md['file_title'] + '.txt', 'w') as text_file:
      text_file.write(textfile)
      
  
  return md

#### Get Url
###################################################################################################
def get_url(string):
    url = string 
    
    if url[:32] == 'https://www.youtube.com/watch?v=':
          id = url[32:]
    elif url[:31] == 'http://www.youtube.com/watch?v=':
          id = url[31:]
    elif url[:16] == 'http://youtu.be/':
          id = url[16:]
    elif url[:17] == 'https://youtu.be/' :
          id = url[17:]
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

###Function Webscrapping Function
######################################################################################################
def get_trans(md):
    

    my_options = webdriver.ChromeOptions()
    #my_options.add_argument('headless')
    my_options.add_argument("--mute-audio")
    my_driver = webdriver.Chrome(executable_path=r'C:\Users\ander\Documents\GitHub\drivers\chromedriver.exe',options=my_options)
    #my_driver = webdriver.Chrome('chromedriver.exe') # In case we need to use in another way

    url = str(md['url'])
    #print(type(url), url)
    my_driver.get(url)

    sleep(1)
    unavail_msg = my_driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/yt-playability-error-supported-renderers/div/yt-player-error-message-renderer/div/div[1]')
    if len(unavail_msg) > 0:
        md['valid link'] = False
                
        my_driver.close()
        return md 
    
        # No video then valid link == False
        
    ## We can insert here the call to thenyputube api
    
    md['id'] = get_url(md['url'])
    md = get_data(md)
    
    #we have to display the transcript button
    agree_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button")[0]
   
    agree_button.click()
    
    #show transcript
       
    
    expand_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button")[0]
    expand_button.click()
    print('here')
    transcript_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer")
    if len(transcript_button) == 0:
        md['valid link'] = True
        md['transc_t'] = 'No data'
        md['transc'] = 'No data'
      
        my_driver.close()
        return md
    else:         

        transcript_button[0].click()
    print('here')
    

    #get transcript text

    my_transcript = my_driver.find_element_by_class_name('style-scope ytd-engagement-panel-section-list-renderer')
    transcript_raw = my_transcript.text
       # format and clean transcript
    tr = transcript_raw.split('\n')
    language = tr[-1]
    del tr[0]
    #del tr[-1]
    time_list = tr[::2]
    text_list = tr[1::2]
    tnt = [s + '\n' for s in text_list]
    tt_list = [str(m) + '   -    ' + str(n) + '\n' for m,n in zip(time_list,text_list)]
    md['transc_t']= ' '.join(tt_list)
    md['transc'] = ' '.join(text_list)
    #print(md['transc'], md['title'], md['language'])
    # format transcript

    #Generate export file
    
    textfile = '\n\nTranscription:\n' + ' ' +md['transc_t']
    
    with open('./BW1/tr/' + md['file_title'] + '.txt', 'a') as text_file:
      text_file.write(textfile)

    my_driver.close()
        
    return md

### Bot functions
#########################################################################################################

@bot.message_handler(commands=['start'])
def start(message):
      #print('Interaction')
      bot.reply_to(message, 'Welcome to the transcript extracting bot. \nPlease send a valid youtube address and you will receive a transcript of the spoken audio.')
  
@bot.message_handler(commands=['help'])
def greetings(message):
  bot.reply_to(message, 'Welcome to the YouTube Transcripter.\n\n You have two ways of giving input:\n a) Give us a valid YouTube address.\n b) Type @vid followed by the topic you want and select your video.\n\nIf the video has a transcription we will deliver it to you ASAP.\n\nPlease be reminded that the adresses type bit.ly or youtu.be are not recognised by the system.')

def youtube(message):
  url = message.text
  if valid_link(url) == True:
    return True
  else:
    bot.reply_to(message, 'This address is not a YouTube link. \n\nPlease supply a a link with the structure \nwww.youtube.com/watch?v=.......\n\n If you need help, please type "/help"')
    return False


@bot.message_handler(func=youtube)
def main_action(message):
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
#  md['url']=message.text
#  md['chat']=message.chat.id
  #print(md)

  md = get_trans(md)
  
  if md['valid link'] == True:
        if md['transc_t'] == 'No data':
          bot.send_message(message.chat.id, 'The requested file has no available transcription. \nPlease try another video link.')
        else:    
          bot.send_message(message.chat.id, 'Your file transcription is delivered in the following file.')
          file_addr = './BW1/tr/' + md['file_title'] + '.txt'
          doc = open(file_addr, 'rb')
          bot.send_document(message.chat.id, doc)
  else:
       bot.send_message(message.chat.id, 'You delivered a link to a not existing video. Please revise your link.') 
bot.polling()
