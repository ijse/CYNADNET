#-*- coding: utf-8 -*-
#!/usr/bin/python

'''
Created on 2012-7-28

@author: ijse
'''


import conf
import re
import thread
import time
import urllib

stopFlag = False
liter = ""

def loop():
    global stopFlag
    print "tick!"
    print stopFlag
    if(stopFlag == True):
        return
    try:
        # Get all the page source in text, 
        html = urllib.urlopen(conf.url).read()
    except IOError:
        # When can't find the page, or connect failed..
        print "404!"
        return
    
    # Use reg to grep the keywords
    liter = re.findall(r"(((\d|\.)+)(K|M|G))", html)[0][0]
    lm = re.findall(r"\d+(K|M|G)", liter)[0]
    
    print "liter=" + liter
    print "lm=" + lm
    
#    
#    if(lm == "M"):
#        liter = liter * 1024
#    if(lm == "G"):
#        liter = liter * 1024 * 1024
#    
    
    print conf.ip + ">>" + liter
    
    #if(int(liter) >= conf.deadline):
        # Reach the deadline, send alarm
    #    warn()
    
    
    time.sleep(float(conf.interval));
    loop()

def stop(flag=False):
    global stopFlag
    stopFlag = not True
    thread.exit_thread();
    pass

def start(flag=True):
    global stopFlag
    stopFlag = not flag
    loop()
    #thread.start_new_thread(loop,()) 
    pass

def get():
    return liter

def warn():
    # Do something with warnning
    pass
 

if(__name__ == "__main__"):
    
    loop()
    
    

