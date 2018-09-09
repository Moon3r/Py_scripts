#!/usr/bin/env python
#coding: utf-=8

import requests
import urllib
import time

url = "http://192.168.254.250"
string = u'连接网络'
string = string.encode('gb2312')
#req = urllib2.Request(url)

#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

payloads = {"DDDDD" : "username","upass" : "password","0MKKey" : string}
pay = urllib.urlencode(payloads)
#response = opener.open(req, pay)
while True:
	response = requests.post(url=url,data=pay)
	print(response.status_code)
	time.sleep(30)
