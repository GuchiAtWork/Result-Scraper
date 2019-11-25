""" File is currently with .pyw execution in hopes to run execution without terminal present 
   on desktop """

import schedule
import time	
import email_send


def autoSend(mailAddr, header, content):
	# Executes email task every 30 seconds
	schedule.every(10).minutes.do(email_send.email, mailAddr, header, content)

	# A while loop needed to keep task running
	while True:

		# Checks whether a task is scheduled to run 
		schedule.run_pending()
		
