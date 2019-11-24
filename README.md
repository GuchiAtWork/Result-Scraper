What is this?

This program is intended only for those who go to the University of Melbourne.

Ideally, this program would check if a student's results has change by inspecting the results page in regular intervals and sending 
emails to said student if it has changed. But this is still working in progress.

These are a list of components I wish to add to the program:

1. web scrape the results using a requests library (DONE)
2. implement a function to calculate the missing grade if WAM has been updated (DONE)
3. implement a scheduler
4. web scrape dates of different semesters (DONE)
5. implement a function to change scheduler settings when current date is not between exam date and results arrival
   (10 minutes when between, 1 day when not)
6. find a way to somehow send results of program to users via email 
7. Implement a GUI for easier user experience
8. To let program handle downloading of modules used in program for easier user experience
