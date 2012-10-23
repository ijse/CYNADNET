#-*- coding: utf-8 -*-
#!/usr/bin/python

'''
Created on 2012-7-28

@author: ijse
'''
import socket

appname = u"NAD网络流量监控(v0.2)"

hidetext = u"程序界面隐藏到了这里:)"
# 
ip = socket.gethostbyname(socket.gethostname())

# check url
url = "http://10.6.125.125/monitor/?sensor_id=1&interval=3600&limit=none&subnet=" + ip
print ip
# check every second
interval = 3 

# the last deadline of MB
deadline = "180M"


print url