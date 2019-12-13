WAM CHECKER INITIAL RELEASE

What is this?

	This program is intended only for those who go to the University of Melbourne.

	Ideally, this program would check if a student's results has change by inspecting the results page in regular intervals and sending emails to said student if it has changed.

	Note that although this program is released, the code has yet been optimised and desirable features
	have not been implemented. I may or may not amend this program in the future.

How do I use this? 

	Before starting, you must download the latest version of Python

	Foremost, download the source code and export it into a new file. 

	Then, go to this website: https://developers.google.com/gmail/api/quickstart/python
	and do only the first step (enable the GMAIL API) using only your UNIMELB gmail account and 
	download the client configuration (within first step). Transfer client configuration file into the
	file you've just made which includes the source file.

	Before launching the source code, you must pip install the following libraries:

		pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib schedule requests beautifulsoup4 

	Now you can execute the source code without any worries, just simply launch checkwam.py using the python
	launcher. (E.g. python "(directory stuff)../(file with source code)/checkwam.py")

When I launched the checkwam.py and inserted my user credentials, I've been suddenly directed to a Google website, is this normal?

	Don't worry, this is normal. What you need to do here is to enable Gmail API, essentially to allow the
	program to use your email to send you results.

A bit of a heads up:

	If you restart your computer, you MUST launch the program again (A bit of a hassle, but you can configure your computer to launch the program when it starts up)

	The program will not run when the computer enters into a sleep state, your computer must virtually run at all times (unless you're willing to buy a virtual private server)

Ignore the below

These are a list of components I wish to add to the program:

1. web scrape the results using a requests library (DONE)
2. implement a function to calculate the missing grade if WAM has been updated (DONE)
3. implement a scheduler (DONE)
4. web scrape dates of different semesters (DONE)
5. find a way to somehow send results of program to users via email (DONE)
6. integrate scheduler and check Wam function 
7. To let program handle downloading of modules used in program for easier user experience
8. Implement GUI for friendlier user experience
	    

