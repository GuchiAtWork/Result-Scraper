import requests
from bs4 import BeautifulSoup
import math
import pickle
import email_send

""" Function intends to webscrape results from UniMelb results page and process data from it """
def check():

	# GET request used to retrieve data for form data, which is used to login results page
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
	URL = "https://prod.ss.unimelb.edu.au/student/login.aspx?ReturnUrl=%2fstudent%2fSM%2fResultsDtls10.aspx%3fr%3d%2523UM.STUDENT.APPLICANT%26f%3d%2524S1.EST.RSLTDTLS.WEB&r=%23UM.STUDENT.APPLICANT&f=%24S1.EST.RSLTDTLS.WEB" 
	response = requests.get(URL, headers = headers)
	soup = BeautifulSoup(response.content, 'html5lib')

	# Retrieving username and password from pickle file
	with open('usercreds', 'rb') as getuser:
		username = pickle.load(getuser)

	with open('passcreds', 'rb') as getpass:
		password = pickle.load(getpass)

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
		# Removing unnecessary details (extra spaces, leaving only relevant data)
		subject_detail = result.find_all('td')
		if subject_detail[6].text in ACCEPTABLEGRADES:
			creditPoints = float(subject_detail[8].text)

			# for the sole purpose of calculating WAM (more creditpoints, more toll on WAM)
			creditCheck = int(creditPoints / NORMALCREDIT)

			score = int(subject_detail[5].text) * creditCheck
			subjects += creditCheck
			totalScore += score

	# Rounding to three decimal places is done for comparison between found and calculated WAM
	calcWam = round(totalScore / subjects, 3)

	return (foundWam, calcWam, totalScore, subjects)

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

""" Function serves to get user's username and password for the purposes of checking result page """
def getAccount():
	username = input("Enter Unimelb Username: ")
	password = input("Enter Unimelb Password: ")

	headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"}
	URL = "https://prod.ss.unimelb.edu.au/student/login.aspx?ReturnUrl=%2fstudent%2fSM%2fResultsDtls10.aspx%3fr%3d%2523UM.STUDENT.APPLICANT%26f%3d%2524S1.EST.RSLTDTLS.WEB&r=%23UM.STUDENT.APPLICANT&f=%24S1.EST.RSLTDTLS.WEB" 
	response = requests.get(URL, headers = headers)
	soup = BeautifulSoup(response.content, 'html5lib')

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

	fileuser = 'usercreds'
	filepass = 'passcreds'

	with open(fileuser, 'wb') as storeuser:
		pickle.dump(username, storeuser) 

	with open(filepass, 'wb') as storepass:
		pickle.dump(password, storepass) 

def main():
	try:
		# checking if credentials are stored in current working directory and creating one if not
		with open('usercreds', 'rb') as getuser:
			username = pickle.load(getuser)		
	except IOError as noCreds:
		getAccount()

		with open('pastWAM', 'wb') as storeWAM:
			pickle.dump(0.000, storeWAM)
	except:
		print("An unexpected error has occured.")
	finally:
		# checking if WAM has been updated and updating users if so
		results = check()

		with open('pastWAM', 'rb') as storeWAM:
			prevWam = pickle.load(storeWAM)

		if (results[0] != prevWam):

			with open('usercreds', 'rb') as getuser:
				username = pickle.load(getuser)

			updatedMarks = find_marks_subjs(results[0], results[2], results[3])

			header = "WAM Update"
			content = "Old WAM: {} -> New WAM: {}\n\n".format(results[1], results[0])

			""" if difference between calculated and found WAM is same (only for instances
				where user is not exactly a new student """

			if (results[0] == results[1]):
				header: "Testing"
				content = "No updates. Just a check"
			else:
				header = "WAM Update"
				content = "Old WAM: {} -> New WAM: {}\n\n".format(results[1], results[0])
				content = "The potential score(s) for {} subject(s): {} marks total".format(
						   updatedMarks[1], updatedMarks[0])

			email_send.email(username+"@student.unimelb.edu.au", header, content)

			with open('pastWAM', 'wb') as storeWAM:
				pickle.dump(results[0], storeWAM) 
		else:
			print("WAM has not been updated")

if __name__ == '__main__':
	main()