from selenium import webdriver
import json
import time
from random import randint

class ScrapeVivino():
	def __init__(self, minNum, maxNum):
		self.browser = webdriver.Firefox()
		self.minNum = minNum
		self.maxNum = maxNum
	# Parses a given website regarding a winery and returns key information
	def getWine(self, url):
		browser = self.browser
		browser.get(url)
		# Wait for 2 to 10 seconds
		time.sleep(randint(self.minNum, self.maxNum))
		try:
			name = browser.find_element_by_css_selector(".winePageHeader__vintage--2Vux3")
			winery = browser.find_element_by_css_selector(".grid__desktop-column-3--Ikdi3:nth-child(1) .anchor__anchor--3DOSm")
		except:
			return None
		region = "N/A"
		try:
			region = browser.find_element_by_css_selector(".grid__desktop-column-3--Ikdi3:nth-child(3) .anchor__anchor--3DOSm").text
		except:
			print("No region available for url:", url)
		style = "N/A"
		try:
			style = browser.find_element_by_css_selector(".grid__desktop-column-3--Ikdi3:nth-child(4) .anchor__anchor--3DOSm").text
		except:
			print("No style available for url:", url)
		rating = "N/A"
		try:
			rating = browser.find_element_by_css_selector(".vivinoRatingWide__averageValue--1zL_5").text
		except:
			print("No rating available for url:", url)
		grapes = "N/A"
		try:
			grapes = browser.find_element_by_css_selector(".grid__desktop-column-3--Ikdi3:nth-child(2) .wineFacts__factHeading--pXg1x+ div")
			grapes = grapes.text.split(",")
			grapes = list(map(str.strip, grapes))
		except:
			print("No grapes available for url:", url)
		pairing = "N/A"
		try:
			pairing = browser.find_element_by_css_selector(".grid__desktop-column-3--Ikdi3:nth-child(5) .wineFacts__factHeading--pXg1x+ div").text
		except:
			print("No pairing available for url:", url)
		imageLink = "N/A"
		try:
			img = browser.find_elements_by_css_selector("img")
			for i in img:
				if i.get_attribute("data-testid") == "deferredHiddenImage":
					imageLink = i.get_attribute("src")
		except:
			print("No image available for url:", url)
		obj = {
			"name": name.text,
			"winery": winery.text,
			"region": region,
			"style": style,
			"rating": rating,
			"grapes": grapes,
			"pairings": pairing,
			"img": imageLink,
			"url": url,
			"updated": True
		}
		return obj

	# Parses a given website regarding a winery and returns key information
	# browser: a browser already open on the page of the url
	# url: url of the browser
	def getWinery(self, url):
		browser = self.browser
		browser.get(url)
		# Wait for 2 to 10 seconds
		time.sleep(randint(self.minNum, self.maxNum))
		try:
			name = browser.find_element_by_css_selector("h1.content-page-header__headline")
		except:
			return None
		avgRate = numWines = "N/A"
		try:
			vals = browser.find_elements_by_css_selector("div.winery-page__header__statistics__item__content__value")
			count = 0
			for i in vals:
				if count%2 == 0:
					avgRate = i.text
				else:
					numWines = i.text
				count += 1
		except:
			print("No average rating of number of wines for url:", url)
		address = "N/A"
		try:
			columns = browser.find_elements_by_css_selector("div.winery-page__contact__content__column__item")
			country = browser.find_element_by_css_selector(".winery-page__contact__content__column__item a")
			for i in columns:
				if i.text != "":
					if i.text == country.text:
						address = address + i.text
						break
					else:
						address = address + i.text + "\n"
		except:
			print("No address for url:", url)
		website = "N/A"
		try:
			website = browser.find_element_by_css_selector(".winery-page__contact__content__column__item--social")
			website = website.get_attribute("href")
		except:
			print("No website for url:", url)
		email = "N/A"
		try:
			email = browser.find_element_by_css_selector(".winery-page__contact__content__column+ .winery-page__contact__content__column div").text
		except:
			print("No email for url:", url)
		latitude = longitude = "N/A"
		try:
			coord = browser.find_element_by_css_selector(".map-canvas")
			latitude = coord.get_attribute("data-lat")
			longitude = coord.get_attribute("data-long")
		except:
			print("No map for url:", url)
		obj = {
			"name": name.text,
			"avgRate": avgRate,
			"numWines": numWines,
			"address": address,
			"longitude": longitude,
			"latitude": latitude,
			"companyWebsite": website,
			"email": email,
			"url": url,
			"updated": True
		}
		return obj

	# Parses a given website regarding a wine region and returns key information
	# browser: a browser already open on the page of the url
	# url: url of the browser
	def getRegion(self, url):
		browser = self.browser
		browser.get(url)
		# Wait for 2 to 10 seconds
		time.sleep(randint(self.minNum, self.maxNum))
		try:
			region = browser.find_element_by_css_selector("h1.content-page-header__headline")
		except:
			return None
		description = "N/A"
		try:
			description = browser.find_element_by_css_selector("div.region-page__header__description__content").text
		except:
			print("No description for region:", url)
		country = "N/A"
		try:
			country = browser.find_element_by_css_selector('a[data-item-type="country"]').text
		except:
			print("No country listed, url:", url)
		obj = {
			"region": region.text,
			"country": country,
			"description": description,
			"url": url,
			"updated": True
		}
		return obj

	# Parses a given website regarding a country and returns key information
	# browser: a browser already open on the page of the url
	# url: url of the browser
	def getCountry(self, url):
		browser = self.browser
		browser.get(url)
		# Wait for 2 to 10 seconds
		time.sleep(randint(self.minNum, self.maxNum))
		try:
			country = browser.find_element_by_css_selector("div.country-page__headline")
		except:
			return None
		obj = {
			"country": country.text,
			"url": url,
			"updated": True
		}
		return obj

	# Parses a given website regarding a country and returns key information
	# browser: a browser already open on the page of the url
	# url: url of the browser
	def getGrape(self, url):
		browser = self.browser
		browser.get(url)
		# Wait for 2 to 10 seconds
		time.sleep(randint(self.minNum, self.maxNum))
		try:
			grape = browser.find_element_by_css_selector("h1.content-page-header__headline")
		except:
			return None
		characteristics = "N/A"
		try:
			characteristics = browser.find_element_by_css_selector("div.content-page-header__sub-header").text
		except:
			print("No characteristics listed, url:", url)
		description = "N/A"
		try:
			description = browser.find_element_by_css_selector("div.grape-page__header__description").text
		except:
			print("No description listed, url:", url)
		origin = "N/A"
		try:
			origin = browser.find_element_by_css_selector("div.grape-page__origin__region").text
			origin = origin + " " + browser.find_element_by_css_selector("div.grape-page__origin__country").text
		except:
			print("No origin listed, url:", url)
		color = "N/A"
		try:
			color = browser.find_element_by_css_selector("figure.grape-color__icon")
			color = color.get_attribute("data-async-image")
			color = "https://vivino.com/" + color
		except:
			print("No color listed, url:", url)
		body = acidity = "N/A"
		try:
			vals = browser.find_elements_by_css_selector("div.characteristic")
			count = 0
			for i in vals:
				if count == 0:
					acidity = i.text.split("\n")[1]
				elif count == 1:
					body = i.text.split("\n")[1]
				count += 1
		except:
			print("No body or acidity listed, url:", url)
		obj = {
			"grape": grape.text,
			"characteristics": characteristics,
			"description": description,
			"acidity": acidity,
			"color": color,
			"body":	body,
			"origin": origin,
			"url": url,
			"updated": True
		}
		return obj

	# Parses a given website regarding a regional style and returns key information
	# browser: a browser already open on the page of the url
	# url: url of the browser
	def getStyle(self, url):
		browser = self.browser
		browser.get(url)
		# Wait for 2 to 10 seconds
		time.sleep(randint(self.minNum, self.maxNum))
		try:
			style = browser.find_element_by_css_selector("h1.content-page-header__headline")
		except:
			return None
		region = "N/A"
		try:
			regionVals = browser.find_element_by_css_selector("div.location").text
			regionVals = regionVals.split('\n')
			region = regionVals[2] + ", " + regionVals[0]
		except:
			print("No region listed, url:", url)
		description = "N/A"
		try:
			description = browser.find_element_by_css_selector("div.wine-style-page__header__description").text
		except:
			print("No description listed, url:", url)
		body = acidity = "N/A"
		try:
			vals = browser.find_elements_by_css_selector("div.characteristic")
			count = 0
			for i in vals:
				if count == 0:
					acidity = i.text.split("\n")[1]
				elif count == 1:
					body = i.text.split("\n")[1]
				count += 1
		except:
			print("No body or acidity listed, url:", url)
		obj = {
			"style": style.text,
			"region": region,
			"description": description,
			"acidity": acidity,
			"body": body,
			"url": url,
			"updated": True
		}
		return obj

	#closes browser
	def close(self):
		self.browser.close()
