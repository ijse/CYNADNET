#!/usr/bin/python
#coding:utf-8

'''
Created on 2012-8-2

@author: liyi_nad
'''
import na_icon
import Checknet
import Taskbar
import conf
import sys
import os
import wx

class CWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, None, -1, title, size = (320, 120), 
                              style= wx.CAPTION | wx.CLOSE_BOX |wx.SYSTEM_MENU | wx.STAY_ON_TOP )
        self.parent = parent;
        self.watchState = False;
        self.pnl = wx.Panel(self)
        
        #self.SetIcon(wx.Icon('wx.ico',wx.BITMAP_TYPE_ICO)) 
        self.SetIcon(na_icon.wx.GetIcon())
        
        itvList = ['5', '30', '60', '120', '180', '300', '600']
        
        self.choice = wx.Choice(self.pnl, -1, (120, 15), choices=itvList)
        self.choice.SetStringSelection("5")
        
        wx.StaticText(self.pnl, -1, u"选择检查间隔时间", (15, 20))
        wx.StaticText(self.pnl, -1, u"秒", (180, 20))
        wx.StaticText(self.pnl, -1, u"达到多少上限时警告", (15, 50))
        wx.StaticText(self.pnl, -1, u"MB/h", (180, 50))
        
        self.button = wx.Button(self.pnl, -1, u"开始监控", pos=(210, 15))
        self.exitBtn = wx.Button(self.pnl, -1, u"退出程序", pos=(210, 45))
        self.deadline = wx.TextCtrl(self.pnl, -1, "180",size=(40, 17), pos=(130, 50)) 
        
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.button)
        self.Bind(wx.EVT_BUTTON, self.OnDestroy, self.exitBtn)
        
        self.taskbar = Taskbar.Taskbar(self)
        self.Bind(wx.EVT_CLOSE, self.OnTaskBar)
        self.checknet = Checknet.Checknet(self.parent.Alarm)
        
        self.taskbar.showTaskbar()
        
    def OnDestroy(self, event):
        self.Hide()
        self.taskbar.hideTaskbar()
        self.checknet.kill()
        sys.exit()
        
    def OnTaskBar(self, event):
        # 隐藏窗口
        self.Show(False)
        # 显示托盘图标
        self.taskbar.showBalloon(conf.appname, u"还在运行，在这里~~", 0)
        #self.taskbar.showTaskbar()
        
    def OnStart(self, event):
        #print "start!!"
        
        self.watchState = True;
        
        conf.interval = self.choice.GetStringSelection()
        self.choice.Disable()
        self.deadline.Disable()
        
        self.Bind(wx.EVT_BUTTON, self.OnStop, self.button)
        self.button.SetLabel(u"停止监控")
        
        # 开启监控
        conf.deadline = self.deadline.GetValue() + "M"
        self.checknet = Checknet.Checknet(self.parent.Alarm)
        self.checknet.start()
        
        # 隐藏窗口
        self.Show(False)
        
        # 显示托盘图标气泡
        #self.taskbar.showTaskbar()
        self.taskbar.showBalloon(conf.appname, u"  已经开启监控...\n 左键单击：显示当前流量\n 右键单击：显示控制菜单", 0)
        pass
    
    def OnStop(self, event):
        #print "stop!!"
        self.watchState = False
        
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.button)
        self.choice.Enable()
        self.deadline.Enable()
        self.button.SetLabel(u"开始监控")
        self.checknet.kill()
        self.taskbar.showBalloon(conf.appname, u"已经停止监控~", 0)
        pass

    def conView(self):
        self.Bind(wx.EVT_BUTTON, self.OnConNet, self.button)
        self.choice.Enable()
        self.deadline.Enable()
        self.button.SetLabel(u"重新连接")
        pass
    
    def OnConNet(self, event):
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.button)
        self.button.SetLabel(u"开始监控")
        os.system("ipconfig /renew")
        pass
        