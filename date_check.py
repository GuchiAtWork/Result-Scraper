from datetime import date
import requests
from bs4 import BeautifulSoup
from enum import Enum

url = "https://www.unimelb.edu.au/dates"

# text present in unimelb dates website to scrape specific dates from
activities = ["Examinations", "Semester 1", "Results final release date"]
exception = "Special"

# Time to activate 
TTA = []

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')

# scraping out dates listed in Unimelb dates
dates = soup.tbody.find_all('tr', attrs = {'class': ''})

fromDate = None
toDate = None
dateOrder = 1

for date in dates:
	eventName = date.find('span', attrs = {'itemprop': 'name'}).text

	# To prevent date in Special/Supplmentary Examinations from being appended to TTA
	if exception in eventName:
		continue

	for activity in activities:
		if activity in eventName:

			# To determine date in which program activates
			if (dateOrder % 2 != 0):
				fromDate = date.find('span', attrs = {'itemprop': 'startTime'}).text
			elif (dateOrder % 2 == 0):
				toDate = date.find('span', attrs = {'itemprop': 'startTime'}).text 
				TTA.append((fromDate, toDate))

			dateOrder += 1
			break


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
