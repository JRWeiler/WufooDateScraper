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

#This program is used to scrape the entries in a wufoo form and look for strings
#being used as dates that are on or after "today minus x" number of days.

#Our use case for this program is that we were using Wufoo to allow someone to register for
#events. We wanted to have the user select from a drop down box of available dates, but
#we cannot use date conditions as selection criteria on non-date type fields. We couldn't use
#a date picker field because this would have allowed the user to select any date, not just those we specified.
#Since a user might be registering for an event date weeks or months in advance, it was not always easy to find
#registrations for recent events in our entry list.
#Using this program, we could see who had registered for an event date within the last week and follow up
#appropriately
#This could also be easily modified to look for name of individuals who have registered for upcoming events.

#Function to create a timestamp for use in the filename
#Returns a timestamp string
def getTimeStamp():
	now = datetime.datetime.now()
	timestamp = str(now.month) + "-" + str(now.day) + "-" + str(now.year) + "[" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + "]"
	return timestamp

#Function that makes the HTTP call. Accepts the name of your wufoo form
#and a URL string. Returns a JSON response object 
#Replace 'youraccount' with your wufoo account name
#Replace APIKey with your API Key
def getData(formName,url):
	ec = requests.get('https://youraccount.wufoo.com/api/v3/forms/'+formName+url,
	auth=('APIKey', 'youraccount'), verify = False)
	return ec.json()

#Wufoo is limited in the number of entries in can return in one call.
#This function determines the total number of entries and decides how many 
#calls (pages) will need to be made. Accepts JSON  response object
#Returns a number of pages integer
def setPages(entries):
	entryCount = entries["EntryCount"]
	pagesBuffer = int(entryCount) / 100
	pagesBuffer = math.floor(pagesBuffer)
	pages = int(pagesBuffer) + 2
	return pages

#Function to create a file on the users desktop with a timestamp and the form name
#Returns a file object
def createFile(timestamp,formName):
	outfile = open(os.path.expanduser("~/desktop/"+formName+"-"+timestamp + ".txt"), "w")
	return outfile

#Main function to scrape through the entries in a wufoo form and look for date values
#in a historic range the user specifies. Accepts a form name string
#and number of days to scrape integer. Does not return anything, but writes information
#to the a file object
def scrapeEntries(formName, daysToScrape):
	outfile = createFile(getTimeStamp(),formName)
	entryCount = getData(formName, "/entries/count.json")
	pages = setPages(entryCount)

	for index in range(0,pages):
		entries = getData(formName, "/entries.json?pageStart="+str(index)+"00&pageSize=99")
		for x in entries["Entries"]:
			try:
				#Replace Field#Date with the field number associated with the date
				#Replace Field#Fname and Field#Lname with the field numbers associated with
				#first and last name respectively.
				#You need to change the format (ex. "%A, %B %d, %Y") to match how the date is written in your wufoo form. 
				#These formatting directives can be found at https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
				registerDate = datetime.datetime(*time.strptime(x["Field#Date"],"%A, %B %d, %Y")[:6])
				print x["Field#Fname"] + " " + x["Field#Lname"]

				#If you want to check for upcoming dates, modify the logical operators in this if statement
				if registerDate > (datetime.datetime.now() - timedelta(days=daysToScrape)) and registerDate <= datetime.datetime.now():
					entryString = x["Field#Fname"] + " " + x["Field#Lname"] + ": " + x["Field#Date"]
					outfile.write(entryString.encode("utf8") + "\n")
			except ValueError:
				continue

	outfile.close()

#Call to main function retrieving user input to pass as parameters
scrapeEntries('-'.join(raw_input("Enter the form name: ").lower().split(" ")),int(raw_input("Enter the number of days to scrape: ")))


