# -*- coding: utf-8 -*-

import requests
import random
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

url = 'https://wxkxsw.com/'
email = 'your_email_address'

def login():
	req = requests.session()

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
	}
	req.get(url=url+'auth/login', headers=headers, verify=False)
	data = {
		'email': email,
		'passwd': 'password',
		'code': ''
	}

	res = req.post(url=url+'auth/login', data=data, headers=headers, timeout=5, verify=False)
	result = json.loads(res.content)
	if result['ret']:
		print("[+] " + result['msg'])
		return req
	return False

def checkin(req):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
	}

	res = req.post(url=url+'user/checkin', verify=False)
	result = json.loads(res.content)
	return result['msg']

def loop_check():
	req = login()
	if req:
		ret = checkin(req)
		exit('[+] ' + ret)
	else:
		exit('[-] Login Failed.')

def check_error():
	mail_host = "smtp.xxx.com"
	mail_pass = "xxxffaxfda"
	sender = email
	receivers = ['xxx@xxx.com']

	message = MIMEText("<a href='" + url + '>check goes wrong.</a>', 'html', 'utf-8')
	message['From'] = Header(sender)
	message['To'] = Header('RecvChecker')

	subject = 'AutoChecker Error'
	message['Subject'] = Header(subject, 'utf-8')

	try:
		send_email = smtplib.SMTP()
		send_email.connect(mail_host, 25)
		send_email.login(sender, mail_pass)
		FLAG04.sendmail(sender, receivers, message.as_string())
	except smtplib.SMTPException as e:
		exit(e)

if __name__ == '__main__':
	while True:
		try:
			loop_check()
			time_to_sleep_rand = random.randint(-3600,3600)
			time.sleep(86400 + time_to_sleep_rand)
		except:
			check_error()

