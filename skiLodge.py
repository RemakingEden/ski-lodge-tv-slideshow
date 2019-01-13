#!usr/bin/python3

"""Script to show weather. avalanche info and lift status in the morning and ski films in the evening"""

import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import schedule
import os
import vlc

url1 = 'http://niseko.nadare.info/'
url2 = 'https://www.windy.com/?43.044,141.348,5,i:pressure,p:off'
url3 = 'https://www.niseko.ne.jp/en/niseko-lift-status/'
intervalAmount = 30
chromeDriverLocation = "/etc/chromium-browser/chromeDriver/chromedriver"
timeToSwitch = "10:55"
vlcPlaylist = "/home/denada/Desktop/fg.mkv" #"/home/pi/Movies/playlist"

options = Options()
options.add_argument("--kiosk")
options.add_argument('disable-infobars')
driver = webdriver.Chrome(chromeDriverLocation, chrome_options=options)

def open_WLA (url1,url2,url3):
	'''opens the links for weather, lift status and avalanche'''
	
	driver.execute_script("window.open('about:blank', 'tab1');")
	driver.switch_to.window("tab1")
	driver.get(url1)
	driver.execute_script("window.open('about:blank', 'tab2');")
	driver.switch_to.window("tab2")
	driver.get(url2)
	driver.execute_script("window.open('about:blank', 'tab3');")
	driver.switch_to.window("tab3")
	driver.get(url3)
	element = driver.find_element_by_id("liftArea")
	driver.execute_script("arguments[0].scrollIntoView();", element)
	return

def switch_tabs(interval):
	'''switches between the WLA tabs on a specific time frame'''
	while True:
		driver.switch_to.window("tab1")
		time.sleep(interval)
		driver.refresh()
		change_program_set_time(timeToSwitch)
		driver.switch_to.window("tab2")
		time.sleep(interval)
		change_program_set_time(timeToSwitch)
		driver.switch_to.window("tab3")
		time.sleep(interval)
		change_program_set_time(timeToSwitch)
	return

def open_play_VLC():
	'''Open and play a VLC playlist'''
	os.system("vlc %a -f --no-audio" % vlcPlaylist)
	pass

def screen_on_off():
	'''checks if the monitor is off or on and pause the program if off'''
	pass

def change_program_set_time(changeTime):
	'''change programs at a specific time'''
	schedule.every().day.at(changeTime).do(open_play_VLC)
	schedule.run_pending()
	return

def main():
    """Main entry point for the script."""
    open_WLA(url1,url2,url3)
    switch_tabs(intervalAmount)
    return

if __name__ == '__main__':
	sys.exit(main())