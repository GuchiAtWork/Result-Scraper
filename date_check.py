import requests
from bs4 import BeautifulSoup
from enum import Enum
from datetime import date

class Month(Enum):
	January = 1
	February = 2
	March = 3
	April = 4
	May = 5
	June = 6
	July = 7
	August = 8
	September = 9
	October = 10
	November = 11
	December = 12

def changeType(string, currentYear):
	splitDate = string.split()
	event = date(int(currentYear), Month[splitDate[2]].value, int(splitDate[1]))
	return event

def convertDateType(dateElement, currentYear):
	fromDate = changeType(dateElement[0], currentYear)
	toDate = changeType(dateElement[1], currentYear)	
	return (fromDate, toDate)

# Time to activate (in Date type)
TTA = []

def scrapeDates():
	# Time to activate (in String type) 
	TTAs = []

	url = "https://www.unimelb.edu.au/dates"

	# text present in unimelb dates website to scrape specific dates from
	activities = ["Examinations", "Semester 1", "Results final release date"]
	exception = "Special"

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html5lib')

	containYear = soup.find('ul', attrs = {'class': 'search-pagination center'}).find('li', attrs = {'class': 'act'}).text
	currentYear = containYear.split()[0]

	# scraping out dates listed in Unimelb dates
	events = soup.tbody.find_all('tr', attrs = {'class': ''})

	fromDate = None
	toDate = None
	dateOrder = 1

	for event in events:
		eventName = event.find('span', attrs = {'itemprop': 'name'}).text

		# To prevent date in Special/Supplmentary Examinations from being appended to TTA
		if exception in eventName:
			continue

		for activity in activities:
			if activity in eventName:

				# To determine dates in which program activates
				if (dateOrder % 2 != 0):
					fromDate = event.find('span', attrs = {'itemprop': 'startTime'}).text
				elif (dateOrder % 2 == 0):
					toDate = event.find('span', attrs = {'itemprop': 'startTime'}).text 
					TTAs.append((fromDate, toDate))

				dateOrder += 1

				# break implemented because activity already found, hence no need to loop
				break

	TTA = [convertDateType(dates, currentYear) for dates in TTAs]
	print(TTA)

