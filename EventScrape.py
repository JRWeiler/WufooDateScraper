import json
import datetime
from datetime import date, timedelta
import re
import os
import shutil
from subprocess import Popen
import requests
from requests.auth import HTTPBasicAuth
import collections 
import time
import math



def getTimeStamp():
	now = datetime.datetime.now()
	timestamp = str(now.month) + "-" + str(now.day) + "-" + str(now.year) + "[" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + "]"
	return timestamp


def getData(formName,url):
	ec = requests.get('https://youraccount.wufoo.com/api/v3/forms/'+formName+url,
	auth=('APIKey', 'youraccount'), verify = False)
	return ec.json()

def setPages(entries):
	entryCount = entries["EntryCount"]
	pagesBuffer = int(entryCount) / 100
	pagesBuffer = math.floor(pagesBuffer)
	pages = int(pagesBuffer) + 2
	return pages

def createFile(timestamp,formName):
	outfile = open(os.path.expanduser("~/desktop/"+formName+"-"+timestamp + ".txt"), "w")
	return outfile

def scrapeEntries(formName, daysToScrape):
	outfile = createFile(getTimeStamp(),formName)
	entryCount = getData(formName, "/entries/count.json")
	pages = setPages(entryCount)

	for index in range(0,pages):
		entries = getData(formName, "/entries.json?pageStart="+str(index)+"00&pageSize=99")
		for x in entries["Entries"]:
			try:
				registerDate = datetime.datetime(*time.strptime(x["Field#Date"],"%A, %B %d, %Y")[:6])
				print x["Field#Fname"] + " " + x["Field#Lname"]
				if registerDate > (datetime.datetime.now() - timedelta(days=daysToScrape)) and registerDate <= datetime.datetime.now():
					entryString = x["Field#Fname"] + " " + x["Field#Lname"] + ": " + x["Field#Date"]
					outfile.write(entryString.encode("utf8") + "\n")
			except ValueError:
				continue

	outfile.close()

scrapeEntries('-'.join(raw_input("Enter the form name: ").lower().split(" ")),int(raw_input("Enter the number of days to scrape: ")))


