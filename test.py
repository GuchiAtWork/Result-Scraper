import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
URL = """https://prod.ss.unimelb.edu.au/student/login.aspx?ReturnUrl=%2fstudent%2fSM%2fResultsDtls10.aspx%3fr%3d%2523UM.STUDENT.APPLICANT%26f%3d%2524S1.EST.RSLTDTLS.WEB&r=%23UM.STUDENT.APPLICANT&f=%24S1.EST.RSLTDTLS.WEB""" 

login_data = {
	'__EVENTTARGET': 'ctl00$Content$cmdLogin',
	'ctl00$Content$txtUserName$txtText': 'khamaguchi',
	'ctl00$Content$txtPassword$txtText': 'JohnTheBurntTofu123'
}

response = requests.get(URL, headers = headers)
soup = BeautifulSoup(response.content, 'html5lib')

login_data["__EVENTARGUMENT"] = soup.find('input', attrs = {'name': '__EVENTARGUMENT'})['value']
login_data["__VIEWSTATE"] = soup.find('input', attrs = {'name': '__VIEWSTATE'})['value']
login_data["__VIEWSTATEGENERATOR"] = soup.find('input', attrs = {'name': '__VIEWSTATEGENERATOR'})['value']
login_data["__EVENTVALIDATION"] = soup.find('input', attrs = {'name': '__EVENTVALIDATION'})['value']

response = requests.post(URL, data = login_data, headers = headers)
soup = BeautifulSoup(response.content, 'html5lib')
wam_statement = float(soup.find('div', attrs = {'class': 'UMWAMText'}).b.text)
result_table = soup.find('table', attrs = {'id': 'ctl00_Content_grdResultDetails'})
results = result_table.find_all('tr')
results.pop(0)

subjects = 0
totalScore = 0
NORMALCREDIT = 12.5

for result in results:
	subject_detail = result.find_all('td')
	creditPoints = float(subject_detail[8].text)
	creditCheck = int(creditPoints // NORMALCREDIT)
	score = int(subject_detail[5].text) * creditCheck
	subjects += creditCheck
	totalScore += score

print(round(totalScore/subjects, 3))