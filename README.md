What is this?

This program is intended only for those who go to the University of Melbourne.

Ideally, this program would check if a student's results has change by inspecting the results page in regular intervals and sending 
emails to said student if it has changed. But this is still working in progress.

These are a list of components I wish to add to the program:

1. web scrape the results using a requests library (DONE)
2. implement a function to calculate the missing grade if WAM has been updated (DONE)
3. implement a scheduler (DONE)
4. web scrape dates of different semesters (DONE)
5. find a way to somehow send results of program to users via email (DONE)
6. Implement a GUI for easier user experience
7. To let program handle downloading of modules used in program for easier user experience

As of 25/11/2019:
	I need to compartmentalize the access_page func in checkwam.py into smaller functions (too long).
	Also need to integrate all other modules so checker can actually be implemented.
	I've also decided to remove the scheduler's ability to run at different intervals dependent on date
	   --- partly due to the fact that the schedule module I've downloaded can't seem to account for this
	    

