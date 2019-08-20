from datetime import date
import requests
from bs4 import BeautifulSoup

url = "https://www.unimelb.edu.au/dates"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html5lib')

today = type(date.today())

print(soup)