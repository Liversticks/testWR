# PMD WR Tracker
Check it out [here](https://https://pmd-wr-tracker.herokuapp.com/)

Made by Liversticks (Oliver X.)

## Functionality
Run srcscrape.py to fetch the most recent world records for PMD speedrunning categories and store them in the SQLite database.
(As of now, the script is run from my local machine daily. If there are changes in the database, then they will be pushed to production via GitHub).

The Django backend handles retrieving and preparing the HTML templates.
As of now, information is rendered on index.html via a template; Bootstrap styling is used to make the page responsive and look nice.

## To-do
* Automate updating. This will be done in two stages:
	* Move the updating script (srcscrape.py) to the server and have it be called automatically
	* Update the speedrun.com access to use the official REST API, not web scraping
