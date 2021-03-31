# !/usr/bin/python3
import urllib.request
import gzip
# import html5lib
# from requests_html import HTMLSession
# scraping library
from vivinoScraper import ScrapeVivino
# mongo library
from mongo import Mongo
# from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import json
import os

# parses xml files
def parseXML(urlFile_content, browser, mongo, mainFile, urlLogName):
	#if file exists
	try:
		#create file if it doesn't exist and open
		file = open("fileLogs/" + urlLogName + ".txt","r")
		#boolean value for current link
		canStart = False
		#lines of file
		lines = file.readlines()
		#starting url, which is the last stored url in file
		startUrl = ""
		if len(lines) == 0:
			canStart = True
		else:
			startUrl = lines[len(lines)-1].strip()
		#close file and open with write capability
		file.close()
		file = open("fileLogs/" + urlLogName + ".txt","a+")
	except Exception as e:
		print(e)
		startUrl = ""
		canStart = True
		print(urlLogName + ".txt doesn't exist, creating it")
		file = open("fileLogs/" + urlLogName + ".txt","w+")
	try:
		#initialize obj object
		obj = None
		#parse xml file contents build tree the tree of urls
		soup = BeautifulSoup(urlFile_content,'xml')
		for url in soup.find_all('loc'):
			if canStart:
				if "/wine-regions/" in url.text:
					obj = browser.getRegion(url.text)
					if obj is not None:
						mongo.insertRegion(obj)
				elif "/wineries/" in url.text:
					obj = browser.getWinery(url.text)
					if obj is not None:
						mongo.insertWinery(obj)
				elif "/grapes/" in url.text:
					obj = browser.getGrape(url.text)
					if obj is not None:
						mongo.insertGrape(obj)
				elif "/w/" in url.text:
					obj = browser.getWine(url.text)
					if obj is not None:
						mongo.insertWine(obj)
				elif "/wine-styles/" in url.text:
					obj = browser.getStyle(url.text)
					if obj is not None:
						mongo.insertStyle(obj)
				elif "/wine-countries/" in url.text:
					obj = browser.getCountry(url.text)
					if obj is not None:
						mongo.insertCountry(obj)
				#print whatever was inserted
				print("Inserted:\n",obj)
				#add url to current open file
				file.write(url.text + "\n")
			else:
		    	#if this is start url then set canStart true and attempt next url
				if startUrl == url.text:
					canStart = True
	except Exception as e:
		print(e)
		#close everything and exit
		#close main file
		mainFile.close()
		#close current open file
		file.close()
		#close scraper
		browser.close()
		#close mongo
		mongo.close()
		#exit python
		print("There was an error")
		exit(1)


# Opens and reads gzip files
def openGZ(url, browser, mongo, mainFile):
    #open url
    source = urllib.request.urlopen(url)
    #open gzip file
    f=gzip.open(source,'rb')
    #read gzip file
    file_content=f.read()
    #close gzip file
    f.close()
    #split url to extract specific url group
    urlLogName = url.split("nsm/")[1]
    urlLogName = urlLogName.split(".xml")[0]
    parseXML(file_content, browser, mongo, mainFile, urlLogName)


#create scraper object
browser = ScrapeVivino(1,5)
#create mongo object
mongo = Mongo()
#Site Map url
siteMap = "https://www.vivino.com/sitemap.xml"
#request site
source = urllib.request.urlopen(siteMap)
#parse site as xml file
soup = BeautifulSoup(source,'xml')
#If file has been created
try:
	#create file if it doesn't exist and open
	file = open("parsedGzips.txt","r")
	#boolean value for current link
	canStart = False
	#lines of file
	lines = file.readlines()
	#starting url
	startUrl = ""
	if len(lines) == 0:
		canStart = True
	else:
		startUrl = lines[len(lines)-1].strip()
	#close file and open with write capability
	file.close()
	file = open("parsedGzips.txt","a+")
except Exception as e:
	print(e)
	startUrl = ""
	canStart = True
	print("parsedGzips.txt doesn't exist, creating it")
	file = open("parsedGzips.txt","w+")
print("Starting to parse")
#accepted substrings in url links
accepted = ['sitemap_style','sitemap_countries', 'sitemap_grapes', 'sitemap_regions', 'sitemap_wineries', 'sitemap_wines']
for url in soup.find_all('loc'):
	if any(c in url.text for c in accepted):
		# if the right url has been reached on the sitemap or the log file was empty
		if canStart:
			file.write(url.text + "\n")
			openGZ(url.text, browser, mongo, file)
		# waits until the right url is reached in xml sitemap
		elif startUrl == url.text:
			canStart = True
			openGZ(url.text, browser, mongo, file)
print("Everything has been added")
#close file
file.close()
#close scraper
browser.close()
#close mongo
mongo.close()
