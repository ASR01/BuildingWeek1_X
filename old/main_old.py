import os
import telebot
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from time import sleep

#API_KEY = os.environ['API_KEY']
#API_KEY = os.getenv('API_KEY')

fileAPI = open("./BW1/API.txt", "r")
API_KEY = fileAPI.read()
bot=telebot.TeleBot(API_KEY)

###Function Webscrapping Function
######################################################################################################
def get_trans(url):
    

    my_options = webdriver.ChromeOptions()
    my_options.add_argument('headless')
    my_options.add_argument("--mute-audio")
    my_driver = webdriver.Chrome(executable_path=r'C:\Users\ander\Documents\GitHub\drivers\chromedriver.exe',options=my_options)
    #my_driver = webdriver.Chrome('chromedriver.exe') # In case we need to use in another way


    mypage = my_driver.get(url)

    sleep(1)

    # TODO 2 if there is a video under the youtube link
    
    unavail_msg = my_driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/yt-playability-error-supported-renderers/div/yt-player-error-message-renderer/div/div[1]')
    if len(unavail_msg) > 0:
        my_dict = {
        'valid link' : False,
        'url' : url
        }
        my_driver.close()
        return my_dict  
    
    # No video then valid link == False

    #we have to display the transcript button
    agree_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button")[0]
    agree_button.click()
    #Stop playback
    #play_button = my_driver.find_elements_by_class_name('//*[@id="movie_player"]/div[32]/div[2]/div[1]/button')
    
    #play_button.click()

    #show transcript
    
    #Todo 1 check if there is a transcript in the video 
    
    expand_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button")[0]
    expand_button.click()
    
    transcript_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer")
    if len(transcript_button) == 0:
        my_dict = {
        'valid link' : True,
        'transc_t' : 'No data',
        'transc' : 'No data',
        'url' : url
        }
        my_driver.close()
        return my_dict
    else:         

        transcript_button[0].click()
    
    
    
    
    #scroll down to get the number of comments
    #my_driver.execute_script("window.scrollTo(1000,document.body.scrollHeight)"


    #get transcript text

    my_transcript = my_driver.find_element_by_class_name('style-scope ytd-engagement-panel-section-list-renderer')


    #get other variables

    my_title = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string')
    #print(my_title.text)
    
    file_title = my_title.text
    file_title = file_title.replace(' ','_')
    file_title= file_title.replace('-','_')
    file_title = file_title[:20]
    
    

    my_views = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[1]/ytd-video-view-count-renderer/span[1]')
    #print(my_views.text)

    my_inserted_date = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[2]/yt-formatted-string')
    #print(my_inserted_date.text)

    my_positives = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string')
    #print(my_positives.text)

    my_negatives = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string')
    #print(my_negatives.text)

    #my_comments = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/h2/yt-formatted-string/span[1]')
    #print(my_comments.text)

    my_length = my_driver.find_element_by_class_name('ytp-time-duration')
    #my_length = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[29]/div[2]/div[1]/div[1]/span[3]')
    #print(my_length.text)

    my_desc = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[9]/div[2]/ytd-video-secondary-info-renderer/div/ytd-expander/div/div/yt-formatted-string')
    #print(my_desc.text)

                      
    transcript_raw = my_transcript.text
    #print(transcript_raw)
    #type(transcript_raw)

    # format and clean transcript

    tr = transcript_raw.split('\n')
    language = tr[-1]
    del tr[0]
    del tr[-1]
    time_list = tr[::2]
    text_list = tr[1::2]
    tnt = [s + '\n' for s in text_list]
    tt_list = [str(m) + '   -    ' + str(n) + '\n' for m,n in zip(time_list,text_list)]
    tt= ' '.join(tt_list)
    tnt = ' '.join(text_list)
    # format transcript

    my_dict = {
        'valid link' : True,
        'language' : language,
        'views' : my_views.text,
        'pos'   : my_positives.text,
        'neg'   : my_negatives.text,
        'transc_t' : tt,
        'transc' : tnt,
        'length' : my_length.text,
        'description' : my_desc.text,
        'title' :my_title.text,
        'file_title' : file_title,
        'url' : url
    
    }
    
    #Generate export file
    
    textfile = 'Title:\t' + my_dict['title'] + '\n\nCaption Language:\t' + my_dict['language']
    textfile += '\n\nURL:\t' + url
    textfile += '\n\nViews:\t' + my_dict['views'] + '\n\nLength:\t' + my_dict['length']
    textfile += '\n\nPositive Reaction:\t' + my_dict['pos'] + '\n\nNegative Reaction:\t' + my_dict['neg']
    textfile += '\n\nTranscription:\n' + ' ' +my_dict['transc_t']
        
    #print(textfile)
    #filename = "./BW1/tr/ + 
    #with open( title + ".txt", "w") as text_file:
    print('./BW1/tr/' + file_title + '.txt')
    with open('./BW1/tr/' + file_title + '.txt', 'w') as text_file:
      text_file.write(textfile)
    #close browser window
    my_driver.close()
        
    return my_dict

#########################################################################################################
# Bot functions

#todo 3
@bot.message_handler(commands=['start'])
def start(message):
      bot.reply_to(message, 'Welcome to the transcript extracting bot. \nPlease send a valid youtube address and you will receive a transcript of the spoken audio.')
  
@bot.message_handler(commands=['help'])
def greetings(message):
  bot.reply_to(message, 'Welcome to the YouTube Transcripter.\n\n You have two ways of giving input:\n a) Give us a valid YouTube address.\n b) Type @vid followed by the topic you want and select your video.\n\nIf the video has a transcription we will deliver it to you ASAP.\n\nPlease be reminded that the adresses type bit.ly or youtu.be are not recognised by the system.')

def youtube(message):
  request = message.text
  #print(request[:18])
  if request[:32] == 'https://www.youtube.com/watch?v=' or request[:31] == 'http://www.youtube.com/watch?v=' or request[:16] == 'http://youtu.be/' or request[:17] == 'https://youtu.be/' :
    print('It is a youtube link')
    return True
  else:
    bot.reply_to(message, 'This address is not a YouTube link. \n\nPlease supply a a link with the structure \nwww.youtube.com/watch?v=.......\n\n If you need help, please type "/help"')
    return False


@bot.message_handler(func=youtube)
def main_action(message):
  bot.reply_to(message, 'It is a YouTube format address!\n <h1>You</h1> will recibe promptly a message with a text file in it.')
  url = message.text
  # TODO 1 and todo 2  prepare to handle the differences 
  # No transcript 'trascript' == False
  # Not valid address valid link == False
  dict = get_trans(url)
  if dict['valid link'] == True:
        if dict['transc_t'] == 'No data':
          bot.send_message(message.chat.id, 'The requested file has no available transcription. \nPlease try another video link.')
        else:    
          bot.send_message(message.chat.id, 'Your file transcription is delivered in the following file.')
          file_addr = './BW1/tr/' + dict['file_title'] + '.txt'
          doc = open(file_addr, 'rb')
          bot.send_document(message.chat.id, doc)
  else:
       bot.send_message(message.chat.id, 'You delivered a link to a not existing video. Please revise your link.') 
bot.polling()
