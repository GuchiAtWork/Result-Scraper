import requests
from bs4 import BeautifulSoup
import math

""" Function intends to webscrape results from UniMelb results page and process data from it """
def access_page():

	# GET request used to retrieve data for form data, which is used to login results page
	headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
	URL = "https://prod.ss.unimelb.edu.au/student/login.aspx?ReturnUrl=%2fstudent%2fSM%2fResultsDtls10.aspx%3fr%3d%2523UM.STUDENT.APPLICANT%26f%3d%2524S1.EST.RSLTDTLS.WEB&r=%23UM.STUDENT.APPLICANT&f=%24S1.EST.RSLTDTLS.WEB" 
	response = requests.get(URL, headers = headers)
	soup = BeautifulSoup(response.content, 'html5lib')

	username = input("Enter Unimelb Username: ")
	password = input("Enter Unimelb Password: ")

	# form data needed to log in to results page
	login_data = {
		'__EVENTTARGET': 'ctl00$Content$cmdLogin',
		'ctl00$Content$txtUserName$txtText': username,
		'ctl00$Content$txtPassword$txtText': password
	}
	login_data["__EVENTARGUMENT"] = soup.find('input', attrs = {'name': '__EVENTARGUMENT'})['value']
	login_data["__VIEWSTATE"] = soup.find('input', attrs = {'name': '__VIEWSTATE'})['value']
	login_data["__VIEWSTATEGENERATOR"] = soup.find('input', attrs = {'name': '__VIEWSTATEGENERATOR'})['value']
	login_data["__EVENTVALIDATION"] = soup.find('input', attrs = {'name': '__EVENTVALIDATION'})['value']

	response = requests.post(URL, data = login_data, headers = headers)

	""" Tracks redirection status of response object (if correct login provided, will redirect,
        whilst wrong data won't) and if not redirected, will ask for login details again"""
	while not response.history:
		print("Incorrect username or password.")
		username = input("Enter Unimelb Username: ")
		password = input("Enter Unimelb Password: ")
		login_data["ctl00$Content$txtUserName$txtText"] = username
		login_data["ctl00$Content$txtPassword$txtText"] = password
		response = requests.post(URL, data = login_data, headers = headers)

	soup = BeautifulSoup(response.content, 'html5lib')

	foundWam = float(soup.find('div', attrs = {'class': 'UMWAMText'}).b.text)
	result_table = soup.find('table', attrs = {'id': 'ctl00_Content_grdResultDetails'})
	results = result_table.find_all('tr')

	# Removing first element in list because value is not relevant (no grades present)
	results.pop(0)

	subjects = 0
	totalScore = 0
	NORMALCREDIT = 12.5
	ACCEPTABLEGRADES = ("H1", "H2A", "H2B", "H3", "P", "N", "NH")

	for result in results:
		subject_detail = result.find_all('td')
		if subject_detail[6].text in ACCEPTABLEGRADES:
			creditPoints = float(subject_detail[8].text)

			# for the sole purpose of calculating WAM (more creditpoints, more toll on WAM)
			creditCheck = int(creditPoints / NORMALCREDIT)

			score = int(subject_detail[5].text) * creditCheck
			subjects += creditCheck
			totalScore += score

	calcWam = round(totalScore / subjects, 3)
	print(find_marks_subjs(foundWam, totalScore, subjects))

""" Function intends to find the number of subjects released and its corresponding marks once WAM is updated """
def find_marks_subjs(wam, totalScore, totalSubjs):

	# Value used to find if potential scores are legitimate or not (e.g. 79.2 is not but 79.002 is)
	MIN_DIF = 1e-04
	MINSCORE = 0

	highestScore = 99

	# On the basis that a person takes between 1 to 6 subjects in current term
	for subjsTaken in range(1, 7):
		estimatedScore = (wam * (totalSubjs + subjsTaken) - totalScore)
		if (MINSCORE <= estimatedScore <= highestScore):
			# To check if estimatedScore value is close to an integer 
			if math.isclose(estimatedScore, int(estimatedScore), rel_tol = MIN_DIF):
				return (int(estimatedScore), subjsTaken)
		highestScore += 100
	return None

def main():
	access_page()

if __name__ == '__main__':
	main()