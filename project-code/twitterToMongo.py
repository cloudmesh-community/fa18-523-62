from pymongo import MongoClient
from bs4 import BeautifulSoup
import time as time_mod
import re
from selenium import webdriver


connection = MongoClient('localhost', 27017)
db = connection.twitterdb
db.twitter_search.ensure_index("id", unique=False, dropDups=True)
collection = db.twitter_search

browser = webdriver.Chrome(r'C:\webdrivers\chromedriver')

dates=['2018-10-01','2018-10-02','2018-10-03']

queries = [u'%23AFCB',
u'%23AFC',
u'%23arsenalfc',
u'%23gunners',
u'%23coyg',
u'%23BHAFC',
u'%23brightonandhovealbion',
u'%23Clarets',
u'%23BurnleyFC',
u'%23cardiffcity',
u'%23cardiffcityfc',
u'%23CFC',
u'%23chelseafc',
u'%23stamfordbridge',
u'%23CPFC',
u'%23crystalpalacefc',
u'%23EFC',
u'%23evertonfc',
u'%23FulhamFC',
u'%23HTAFC',
u'%23LCFC',
u'%23leicestercity',
u'%23LFC',
u'%23liverpoolfc',
u'%23thekop',
u'%23MCFC',
u'%23mancity',
u'%23manchestercity',
u'%23MUFC',
u'%23MUTD',
u'%23MANU',
u'%23reddevils',
u'%23manutd',
u'%23ggmu',
u'%23NUFC',
u'%23newcastleunitedFC',
u'%23SaintsFC',
u'%23southamptonFC',
u'%23COYS',
u'%23TottenhamHotspur',
u'%23TottenhamHotspurs',
u'%23comeonyouspurs',
u'%23Thfc',
u'%23WatfordFC',
u'%23WHUFC',
u'%23wwfc',
u'%23Wolverhamptonfc',
u'%23WolverhamptonWanderers',
u'%23wolvesfc',
u'%23westhamunited' 
]

def tweet_scroller(url):

    browser.get(url)
    
    
    lastHeight = browser.execute_script("return document.body.scrollHeight")
    
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        
        time_mod.sleep(3)
        newHeight = browser.execute_script("return document.body.scrollHeight")
        
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight
            
    html = browser.page_source

    return html

for query in queries:
   for i in range(len(dates)-1):
     
     base_url = u'https://twitter.com/search?q='
     
     start = dates[i]
     end = dates[i+1]
     filter_by_date = '%20since%3A'+start+'%20until%3A'+end
     url = base_url + query + filter_by_date
     time_mod.sleep(1)
     
     
     soup = BeautifulSoup(tweet_scroller(url), "html.parser")
     
     
     all_tweets = soup.find_all('div',{'class':'tweet'})
     
     
     user_list = []
     time_list = []
     msg_list = []
     tweet_id_list = []
     hash_list = []
     headers_list = ["User","Tweet_id","Timestamp","Message","Hashtags"]
     final_list =[]
     final_list.append(headers_list)
     
     
     for tweet in all_tweets:
        
         content = tweet.find('div',{'class':'content'})
         header = content.find('div',{'class':'stream-item-header'})
         user = re.findall("@\w+",header.find('a',{'class':'account-group js-account-group js-action-profile js-user-profile-link js-nav'}).text.replace("\n"," ").strip())[0]
         time = header.find('a',{'class':'tweet-timestamp js-permalink js-nav js-tooltip'}).prettify()#.find('span').text.replace("\n"," ").strip()
         index1 = time.find('data-conversation-id')
         index2 = time.find('href')
         tweet_id= time[index1+22:index2-2]
         index3 = time.find('title')
         index4 = time.find('span')
         #timestamp = time[index3+7:index4-5]
         message = content.find('div',{'class':'js-tweet-text-container'}).text.replace("\n"," ").strip()
         hashtags = " ".join(re.findall("#[a-zA-Z]+", message))
        
         tweet = {'id':tweet_id, 'username':user, 'text':message, 'hashtags':hashtags,'used_hashtag':query[3:],'created':start, 'dateid':start[0:4]+start[5:7]+start[8:10]}
        
         collection.save(tweet)
