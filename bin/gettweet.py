import requests
import logging
from twython import Twython
from twython import TwythonError
import yaml
from yaml import load

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S') 

# Read configuration and return the conf
def getConfFromFile(conf_file_name):
    try:
        conf_file = open(conf_file_name,'r')
    except IOError:
        logging.error("Error: Open config file: %s failed due to IOError!" % (conf_file_name))
        return None 

    logging.debug("Debug: Open config file: %s successed." % (conf_file_name))
    conf = yaml.load(conf_file)
    logging.debug("Debug: From config file: %s get config: %s." % (conf_file_name,conf))
    
    conf_file.close()
    return conf

# Get value by key
def getConf(conf,section,key):
    if conf == False:
        logging.warning("Warning: Invalid configuration!")
        return ""

    return conf[section][key]

# Get tweet of specific user 
def getNewTweet():
    conf = getConfFromFile("../conf/twitter.yaml")
    if conf == None:
        logging.error("Get null conf from file.")
        return ""

    CONSUMER_KEY = getConf(conf,"user","consumer_key")
    CONSUMER_SECRET = getConf(conf,"user","consumer_secret")
    ACCESS_TOKEN = getConf(conf,"user","access_token")
    ACCESS_SECRET = getConf(conf,"user","access_secret")
    logging.debug("Debug: consumer_key: %s, consumer_secret: %s, access_token: %s, access_secret: %s." % \
                          (CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET))

    twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_SECRET)
    screen_name = getConf(conf,"target","screen_name")

    #Get latest tweet 
    user_tweets = twitter.get_user_timeline(screen_name=screen_name,count=1)
    if len(user_tweets) == 0:
        logging.info("Info: Got no tweet from timeline.")
        return ""

    # twitter.get_user_timeline returns a truncated tweet, we need the untruncated one
    tweet = user_tweets[0]
    tweet = twitter.show_status(id=tweet['id_str'],tweet_mode='extended')
    if tweet == False:
        logging.info("Info: Got no tweet after show_status.")
        return ""
    
    # Search keyword in full tweet
    fulltext = tweet['full_text'].encode('utf-8')
    lower_fulltext = fulltext.lower()
    logging.debug("Debug: Tweet is: %s." % (fulltext))

    keyword = getConf(conf,"target","keyword")
    findresult = lower_fulltext.find(keyword)
    if findresult >= 0:
        logging.debug("Debug: Keyword found in this tweet.")
        return tweet['full_text'].encode('utf-8')
    else:
        logging.debug("Debug: No keyword found in this tweet.")
        return ""

if __name__=="__main__":
    tweet = getNewTweet()
    print tweet
