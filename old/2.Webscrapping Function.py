
from selenium import webdriver
from time import sleep
import datetime

def get_trans(url):
    

    # It si possible to add an execution path to avoid having to insert the chrome into the path

    #change it to make it work everywhere

    my_driver = webdriver.Chrome(executable_path=r'C:\Users\ander\Documents\GitHub\drivers\chromedriver.exe')
    #my_driver = webdriver.Chrome('chromedriver.exe') # In case we need to use in another way


    mypage = my_driver.get(url)

    sleep(1)

    # TODO 2 if there is a video under the youtube link
    # No video then valid link == False

    #we have to display the transcript button
    agree_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]/a/tp-yt-paper-button")[0]
    agree_button.click()
    print(type(agree_button))
    #Stop playback
    #play_button = my_driver.find_elements_by_class_name('//*[@id="movie_player"]/div[32]/div[2]/div[1]/button')
    
    #play_button.click()

    #show transcript
    
    #Todo 1 check if there is a transcript in the video 
    
    expand_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button")[0]
    expand_button.click()
    print(type(expand_button))
    
    transcript_button = my_driver.find_elements_by_xpath("/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer")[0]
    transcript_button.click()
    print(type(transcript_button))

    #scroll down to get the number of comments
    #my_driver.execute_script("window.scrollTo(1000,document.body.scrollHeight)"


    #get transcript text

    my_transcript = my_driver.find_element_by_class_name('style-scope ytd-engagement-panel-section-list-renderer')


    #get other variables

    my_title = my_driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/h1/yt-formatted-string')
    #print(my_title.text)
    

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
        'title' :my_title.text
    
    }
    
    #Generate export file
    
    textfile = 'Title:\t' + my_dict['title'] + '\n\nCaption Language:\t' + my_dict['language']
    textfile = textfile + '\n\nViews:\t' + my_dict['views'] + '\n\nLength:\t' + my_dict['length']
    textfile = textfile + '\n\nPositive Reaction:\t' + my_dict['pos'] + '\n\nNegative Reaction:\t' + my_dict['neg']
    textfile = textfile + '\n\nTranscription:\n' + my_dict['transc_t']
        
    #print(textfile)
    
    #filename = "./BW1/tr/ + 
    with open("./BW1/tr/Transcript.txt", "w") as text_file:

        text_file.write(textfile)
    #close browser window
    #my_driver.close()

    return my_dict

url = 'https://www.youtube.com/watch?v=DejqvrLU6eU'


get_trans(url)

