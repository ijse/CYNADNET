#!/usr/bin/python
#coding:utf-8

'''
Created on 2012-8-2

@author: liyi_nad
'''
import na_icon
from wx import EmptyIcon
import conf
import os
import win32api
import win32con
import win32gui

class Taskbar:
    def __init__(self, owner):
        self.owner = owner
        self.visible = 0
        
        message_map = {
            win32con.WM_DESTROY: self.onDestroy,
            win32con.WM_COMMAND: self.onCommand,
            win32con.WM_USER+20: self.onTaskbarNotify,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "xxx"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        wc.hCursor = win32gui.LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = win32gui.RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow( classAtom, "Taskbar", style, \
                    0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                    0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        
#        icon = win32gui.LoadIcon(0, "wx.ico")
        icon = "wx.ico"
        
#        icon = EmptyIcon()
#        icon.CopyFromBitmap(na_icon.wx.GetBitmap())
        
        if icon is None or not os.path.isfile(icon):
            self.icon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        else:
            self.icon = win32gui.LoadImage(hinst, icon, win32con.IMAGE_ICON, 0,
                                       0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
        
        self.setIcon(self.icon, conf.appname)
        
    def setIcon(self, hicon, tooltip=None):
        self.hicon = hicon
        self.tooltip = tooltip
        
    def showTaskbar(self):
        """Display the taskbar icon"""
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE
        if self.tooltip is not None:
            flags |= win32gui.NIF_TIP
            nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, self.tooltip)
        else:
            nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon)
#        if self.visible:
#            self.hide()
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        self.visible = 1

    def hideTaskbar(self):
        """Hide the taskbar icon"""
        if self.visible:
            nid = (self.hwnd, 0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        self.visible = 0
        
    def onDestroy(self, hwnd, msg, wparam, lparam):
        self.hide()
        win32gui.PostQuitMessage(0) # Terminate the app.

    def onTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP:
            self.onClick()
        elif lparam == win32con.WM_LBUTTONDBLCLK:
            self.onDoubleClick()
        elif lparam ==  win32con.WM_RBUTTONUP:
            self.onRightClick()
        elif lparam == win32con.WM_MOUSEHOVER:
            self.onHover()
            
        return 1

    def onHover(self):
        """Override in subclassess"""
        pass
    
    def onClick(self):
        """Override in subclassess"""
        pass
    def onDoubleClick(self):
        """Override in subclassess"""
        pass
    def onRightClick(self):
        """Override in subclasses"""
        
        if(self.owner.watchState == True):
            statestr = u"停止"
        else:
            statestr = u"开始"
        
        menu = win32gui.CreatePopupMenu()   
        win32gui.AppendMenu( menu, win32con.MF_STRING, 1023, u"显示界面")
        win32gui.AppendMenu( menu, win32con.MF_STRING, 1024, statestr + u"监控")
        win32gui.AppendMenu( menu, win32con.MF_STRING, 1025, u"退出程序" )   
        pos = win32gui.GetCursorPos()   
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp   
        win32gui.SetForegroundWindow(self.hwnd)   
        win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)   
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)   
        pass
    
    def onCommand(self, hwnd, msg, wparam, lparam):   
        commandId = win32api.LOWORD(wparam)   
        if commandId == 1023:   
            # 显示界面
            #self.hideTaskbar()
            self.owner.Show(True)
        elif commandId == 1024:
            # 停止监控
            if(self.owner.watchState == True):
                self.owner.OnStop(None)
            else:
                self.owner.OnStart(None)
            
        elif commandId == 1025:
            # 退出程序
            print "exit"
            self.owner.OnDestroy(None)
            
        else:   
            print "Unknown command -", commandId

    def showBalloon(self, title, content, mtype):
        TYPES = (win32gui.NIF_INFO, 
                 win32gui.NIF_MESSAGE, 
                 win32gui.NIF_STATE,
                 win32gui.NIF_TIP
                 )[mtype]
        
        #NIF_INFO flag below enables balloony stuff
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_INFO
        #define the icon properties (see http://msdn.microsoft.com/library/default.asp?url=/library/en-us/shellcc/platform/shell/reference/structures/notifyicondata.asp)
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, self.hicon, "", content, 10, title, TYPES)
        #change our already present icon ...
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
