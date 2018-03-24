import logging
import sched
import time
from datetime import datetime
import os
from gettweet import getNewTweet
import yaml
from yaml import load

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

buff=""
schedule = sched.scheduler(time.time, time.sleep)

def getConfFromFile(conf_file_name):
    try:
        conf_file = open(conf_file_name,'r')
    except IOError:
        logging.error("Error: Open config file: %s failed." % (conf_file_name))
        return None

    logging.debug("Debug: Open config file: %s successed." % (conf_file_name))
    
    conf = yaml.load(conf_file)
    logging.debug("Debug: From config file: %s get config: %s." % (conf_file_name,conf))

    conf_file.close()
    return conf

def getConf(conf,section,key):
    if conf == False:
        logging.warning("Warning: Invalid configuration!")
        return ""

    return conf[section][key]

def sendNotification(inc):
    global buff

    tweet = getNewTweet()
    if buff != tweet:
        logging.info("Info: There is a new tweet.")
        os.system("sh sendmessage.sh \"" + tweet + "\"")
        #os.system("sh echo.sh \"" + tweet + "\"")
        buff=tweet
    schedule.enter(inc, 0, sendNotification, (inc,))

def sch(inc=60):                
    schedule.enter(0, 0, sendNotification, (inc,))
    schedule.run()

if __name__=="__main__":
    conf = getConfFromFile("../conf/timer.yaml")
    inc = getConf(conf,"timer","inc")
    sch(300)
    
