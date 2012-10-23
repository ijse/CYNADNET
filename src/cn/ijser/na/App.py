#-*- coding: utf-8 -*-
#!/usr/bin/python

'''
Created on 2012-8-2

@author: liyi_nad
'''


import Window
import conf
import os
import wx

class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, 0)
        return None
    
    def OnInit(self):
        self.frame = Window.CWindow(self, u"NAD网络流量监控 for " + conf.ip)
        self.frame.Show()
        self.frame.taskbar.onClick = self.onIconClick
        return True
    
    def Alarm(self, num):
        #print "Sound Alarm!!!"
        self.frame.conView()
        self.frame.taskbar.showBalloon(conf.appname, u"您的网络流量 已经超出！自动为您断开网络以防止被封网。", 2)
        os.system("ipconfig /release")
        pass
    
    def onIconClick(self):
        #print "clicked!!"
        self.frame.taskbar.showBalloon(conf.appname, u"正在获取，请稍候...", 0)
        n = self.frame.checknet.getNetnum()
        self.frame.taskbar.showBalloon(conf.appname, u"您当前网络流量是：" + n + "/h", 0)
        

if(__name__ == "__main__"):
    app = MyApp()
    app.MainLoop()
    