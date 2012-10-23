#coding=utf-8

from threading import Thread
import conf
import re
import time
import urllib

class Checknet(Thread):
    def __init__(self, alarm):
        self.isStart = True
        self.alarm = alarm
        self.netnum = "-"
        Thread.__init__(self)
        pass
    
    def run(self):
        '''
            Start watch ...
        '''
        while self.isStart:
            html = self.fetchHtml(conf.url)
            num1 = self.grepData(html)
            num2 = self.fmtData(conf.deadline)
            
            rslt = self.compare(num1, num2)
            
            #print ">>", num1, num2, rslt
            
            if(rslt >= 0):
                self.alert(num1)
                return 
            self.netnum = num1;
            time.sleep(float(conf.interval));
        pass
    def kill(self):
        self.isStart = False
    def alert(self, num):
        '''
            Sound ALARM!!
        '''
        self.alarm(num)
    
    def getNetnum(self):
        '''
            Get ...
            update: 返回最新的数据，而不是缓存的
        '''
        html = self.fetchHtml(conf.url)
        num1 = self.grepData(html)
        
        return num1[0]
    
    
    def compare(self, num1, num2):
        '''
            Compare two nums in different lm
        '''
        order = ["B", "K", "M", "G"]
        try:
            i1 = order.index(num1[2])
        except ValueError:
            return 1
        
        i2 = order.index(num2[2])
        
        if(i1 == i2):
            return num1[1] - num2[1]
        elif(i1 < i2): #K,M
            return num1[1] - num2[1]*1024**(i2-i1)
        elif(i1 > i2): #M,K
            return num1[1]*1024**(i1-i2) - num2[1]
        else:
            return 1
    
    def fmtData(self, dtn):
        '''
            format: 180MB => ("180M", 180, "M")
        '''
        #print ">>dtn=", dtn
        lm = re.findall(r"[\d.]+(K|M|G)", dtn)[0]
        return (dtn, float(dtn.replace(lm,"")), lm)
    
    def grepData(self, html):
        '''
            Get Data from html
        '''
        # Use reg to grep the keywords
        liter = re.findall(r"(((\d|\.)+)(K|M|G))", html)[0][0]
        return self.fmtData(liter)
    
    def fetchHtml(self, url):
        '''
            Get HTML from remote server
        '''
        try:
            # Get all the page source in text, 
            html = urllib.urlopen(url).read()
        except IOError:
            # When can't find the page, or connect failed..
            #print "404! Network Error!"
            self.isStart = False
            raise IOError("404")
        return html
        

if(__name__ == "__main__"):
    
    def alarm(num):
        print "I got alert:" , num
    
    c = Checknet(alarm)
    
    c.start()
    print "Wait 3s..."
    time.sleep(3)
    c.kill()
    print "killed"
    time.sleep(2)
    c.start()
    print "Start again.."
    
    
    ''' Check Test '''
    c = Checknet()
    html = c.fetchHtml(conf.url)
    
    print "Test c.fetchHtml(url)"
    print html
    print 
    print 
    
    print "Test c.grepData(html)"
    print c.grepData(html)
    print 
    print 
    
    print "Test c.fmtData('180M')"
    print c.fmtData("180G")
    print 
    print 

    
    print "Test c.compare(a. b)"
    nlist = [("1M", "1M"), ("1M", "2M"),
            ("1M", "1K"), ("1M", "1G"),
            ("1K", "1G"), ("1K", "1G") ]
    for d in nlist:
        a = c.fmtData(d[0])
        b = c.fmtData(d[1])
        print a , "-" , b , "=" , str(c.compare(a, b))
    
    pass
    
