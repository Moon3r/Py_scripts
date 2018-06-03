#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = 'MoR03r'

import requests
import re
import time

def verify(ip, port, ip_type, count):
	try:
		proxies = {ip_type: ip_type + '://' + ip + ':' + port,}
		start = time.time()
		results = requests.get("http://ip111.cn", proxies=proxies, timeout=5)
		stop = time.time()
		xxx = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', results.content)
		try:
			if xxx[0] == ip:
				time_use = str(int((stop-start)*100000)/100.0)
				if len(time_use) < 8:
					for i in range(8-len(time_use)):
						time_use = ' ' + time_use
				print '[+] TIME:%sms IP:%15s  PORT:%5s  TYPE:%5s' % (time_use, ip, port, ip_type)
				return '\'' + ip_type + '\': \'' + ip_type + '://' + ip + ':' + port + '\',\n'
		except:
			return 0
	except:
		return 0

def get_ip(count_dst):
	count = count_dst
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
	}
	file_save = open('proxy_ip.txt', 'a')
	file_save.write('{\n')
	page = 1
	while True:
		results = requests.get("http://www.xicidaili.com/nn/" + str(page), headers=headers)
		xxx = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}.*\s.*\s.*\s.*\s.*\s.*\s.*', results.content)
		for i in xxx:
			ip = re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', i)[0]
			port = re.findall('\d{1,5}', i)[4]
			types = re.findall('(HTTPS)|(HTTP)' , i)[0]
			ip_type = ''
			if types[0] != '':
				ip_type = types[0]
			else:
				ip_type = types[1]
			status = verify(ip, port, ip_type.lower(), count_dst-count+1)
			if bool(status) == 1:
				count -= 1
				file_save.write('\t' + status)
				if not count:
					file_save.write('}')
					file_save.close()
					return 1
		page += 1

if __name__ == '__main__':
	count = raw_input('[*] Input how many you want to get: ')
	start = time.time()
	status = get_ip(int(count))
	if status:
		stop = time.time()
		print('[+] Time use: %.3fs\n[+] Finished!' % (stop-start))
