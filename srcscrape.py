#!
# srcscrape.py
# Obtains WR times and runner names from sr.c
# BETA 3.0: Updates information in provided SQLite database file

# Oliver X. (Liversticks)

from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import os
import sqlite3

# Leaderboards are Normally dynamically generated. However, they can be accessed via below static pages:

# Blue Rescue Team and Red Rescue Team

# any%, No WM No QS
rtENGanySS = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6868&game=pmdredblue&verified=1&category=3035&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# any%, No WM
rtENGanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=94552&game=pmdredblue&verified=1&category=3035&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# any%, Unrestricted
rtENGanyUR = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6867&game=pmdredblue&verified=1&category=3035&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# any% JPN, No WM No QS
rtJPNanySS = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6868&game=pmdredblue&verified=1&category=88521&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# any% JPN, No WM
rtJPNanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=94552&game=pmdredblue&verified=1&category=88521&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# any% JPN, Unrestricted
rtJPNanyUR = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6867&game=pmdredblue&verified=1&category=88521&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# All Icons, No WM No QS
rtENGiconsSS = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6868&game=pmdredblue&verified=1&category=32380&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# All Icons, No WM
rtENGiconsNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=94552&game=pmdredblue&verified=1&category=32380&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# All Icons, Unrestricted
rtENGiconsUR = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6867&game=pmdredblue&verified=1&category=32380&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# REA, No WM No QS
rtENGreaSS = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6868&game=pmdredblue&verified=1&category=74562&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# REA, No WM
rtENGreaNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=94552&game=pmdredblue&verified=1&category=74562&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# REA, Unrestricted
rtENGreaUR = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6867&game=pmdredblue&verified=1&category=74562&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# Low%, Unrestricted
rtENGlowUR = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6867&game=pmdredblue&verified=1&category=60218&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='
# All Dungeons, No WM No QS
rtENGadSS = 'https://www.speedrun.com/ajax_leaderboard.php?variable2121=6868&game=pmdredblue&verified=1&category=69329&region=&platform=&variable251=&emulator=0&video=&obsolete=&date='

# Explorers of Time and Explorers of Darkness

# any%, WM
tdENGanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64433&variable30535=102484&variable30536=102486&variable31003=104426&game=pmdtimedarkness&verified=1&category=3049&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# any%, No WM
tdENGanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102484&variable30536=102486&variable31003=104426&game=pmdtimedarkness&verified=1&category=3049&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# any% JPN, WM
tdJPNanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102484&variable30536=102486&variable31003=104425&game=pmdtimedarkness&verified=1&category=88526&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# any% JPN, No WM
tdJPNanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102484&variable30536=102486&variable31003=104426&game=pmdtimedarkness&verified=1&category=88526&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# Darkrai, WM
tdENGdarkWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102483&variable30536=102486&variable31003=104425&game=pmdtimedarkness&verified=1&category=87239&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# Darkrai, No WM
tdENGdarkNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102484&variable30536=102486&variable31003=104425&game=pmdtimedarkness&verified=1&category=87239&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# REA, unlimited WM
tdENGreaUW = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102483&variable30536=102485&variable31003=104425&game=pmdtimedarkness&verified=1&category=87241&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='
# REA, minimum WM
tdENGreaMW = 'https://www.speedrun.com/ajax_leaderboard.php?variable19600=64434&variable30535=102483&variable30536=102486&variable31003=104425&game=pmdtimedarkness&verified=1&category=87241&region=&platform=&variable6446=&emulator=0&video=&obsolete=&date='

# Explorers of Sky

# any%, WM
skyENGanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65386&variable22018=72935&variable27650=93444&variable31004=104428&variable37354=126157&game=pmdsky&verified=1&category=3050&region=&platform=&emulator=0&video=&obsolete=&date='
# any%, No WM
skyENGanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50768&variable19867=65386&variable22018=72935&variable27650=93444&variable31004=104428&variable37354=126157&game=pmdsky&verified=1&category=3050&region=&platform=&emulator=0&video=&obsolete=&date='
# any% JPN, WM
skyJPNanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65386&variable22018=72935&variable27650=93444&variable31004=104427&variable37354=126157&game=pmdsky&verified=1&category=88527&region=&platform=&emulator=0&video=&obsolete=&date='
# any% JPN, No WM
skyJPNanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65386&variable22018=72935&variable27650=93444&variable31004=104428&variable37354=126157&game=pmdsky&verified=1&category=88527&region=&platform=&emulator=0&video=&obsolete=&date='
# Darkrai, WM
skyENGdarkWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65386&variable22018=72935&variable27650=93444&variable31004=104427&variable37354=126157&game=pmdsky&verified=1&category=48164&region=&platform=&emulator=0&video=&obsolete=&date='
# Darkrai, No WM
skyENGdarkNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72935&variable27650=93444&variable31004=104427&variable37354=126157&game=pmdsky&verified=1&category=48164&region=&platform=&emulator=0&video=&obsolete=&date='
# Darkrai JPN, WM
skyJPNdarkWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72935&variable27650=93444&variable31004=104427&variable37354=126156&game=pmdsky&verified=1&category=98801&region=&platform=&emulator=0&video=&obsolete=&date='
# Darkrai JPN, No WM
skyJPNdarkNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72935&variable27650=93444&variable31004=104427&variable37354=126157&game=pmdsky&verified=1&category=98801&region=&platform=&emulator=0&video=&obsolete=&date='
# REA, WM
skyENGreaWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72935&variable27650=93444&variable31004=104427&variable37354=126156&game=pmdsky&verified=1&category=82042&region=&platform=&emulator=0&video=&obsolete=&date='
# REA, No WM
skyENGreaNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72935&variable27650=93445&variable31004=104427&variable37354=126156&game=pmdsky&verified=1&category=82042&region=&platform=&emulator=0&video=&obsolete=&date='
# All Icons, WM
skyENGiconsWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72935&variable27650=93445&variable31004=104427&variable37354=126156&game=pmdsky&verified=1&category=71260&region=&platform=&emulator=0&video=&obsolete=&date='
# All Icons, No WM
skyENGiconsNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72936&variable27650=93445&variable31004=104427&variable37354=126156&game=pmdsky&verified=1&category=71260&region=&platform=&emulator=0&video=&obsolete=&date='
# All Special Episodes
skyENGase = 'https://www.speedrun.com/ajax_leaderboard.php?variable15249=50769&variable19867=65385&variable22018=72936&variable27650=93445&variable31004=104427&variable37354=126156&game=pmdsky&verified=1&category=18548&region=&platform=&emulator=0&video=&obsolete=&date='

# WiiWare
wiiJPNany = 'https://www.speedrun.com/ajax_leaderboard.php?game=pmdwii&verified=1&category=6565&region=&platform=&variable593=&emulator=2&video=&obsolete=&date='

# Gates to Infinity

# any%, WM
gtiENGanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable37118=125354&variable40725=139147&variable40726=139148&game=pmdgti&verified=1&category=3045&region=&platform=&emulator=0&video=&obsolete=&date='
# any%, No WM
gtiENGanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable37118=125355&variable40725=139147&variable40726=139148&game=pmdgti&verified=1&category=3045&region=&platform=&emulator=0&video=&obsolete=&date='
# any% JPN, WM
gtiJPNanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable37118=125354&variable40725=139146&variable40726=139148&game=pmdgti&verified=1&category=88528&region=&platform=&emulator=0&video=&obsolete=&date='
# any% JPN, No WM
gtiJPNanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable37118=125354&variable40725=139147&variable40726=139148&game=pmdgti&verified=1&category=88528&region=&platform=&emulator=0&video=&obsolete=&date='
# REA, WM
gtiENGreaWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable37118=125354&variable40725=139146&variable40726=139148&game=pmdgti&verified=1&category=91144&region=&platform=&emulator=0&video=&obsolete=&date='
# REA, No WM
gtiENGreaNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable37118=125354&variable40725=139146&variable40726=139149&game=pmdgti&verified=1&category=91144&region=&platform=&emulator=0&video=&obsolete=&date='

# Super Mystery Dungeon

# any%, WM
smdENGanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable24326=81503&variable24328=81505&variable31005=104429&game=psmd&verified=1&category=19402&region=&platform=&emulator=2&video=&obsolete=&date='
# any%, No WM
smdENGanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable24326=81504&variable24328=81505&variable31005=104429&game=psmd&verified=1&category=19402&region=&platform=&emulator=2&video=&obsolete=&date='
# any% JPN, WM
smdJPNanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable24326=81503&variable24328=81505&variable31005=104429&game=psmd&verified=1&category=88529&region=&platform=&emulator=2&video=&obsolete=&date='
# any% JPN, No WM
smdJPNanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable24326=81503&variable24328=81505&variable31005=104430&game=psmd&verified=1&category=88529&region=&platform=&emulator=2&video=&obsolete=&date='
# 100%, WM
smdENG100WM = 'https://www.speedrun.com/ajax_leaderboard.php?variable24326=81503&variable24328=81505&variable31005=104430&game=psmd&verified=1&category=75625&region=&platform=&emulator=2&video=&obsolete=&date='
# as of Now No 100%, No WM category exists

# Rescue Team DX

# any%, WM
rtdxENGanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable40519=138361&game=pmddx&verified=1&category=105777&platform=&variable40520=&emulator=0&video=&obsolete=&date='
# any%, No WM
rtdxENGanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable40519=138362&game=pmddx&verified=1&category=105777&platform=&variable40520=&emulator=0&video=&obsolete=&date='
# any% JPN, WM
rtdxJPNanyWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable40519=138361&game=pmddx&verified=1&category=105793&platform=&variable40520=&emulator=0&video=&obsolete=&date='
# any% JPN, No WM
rtdxJPNanyNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable40519=138362&game=pmddx&verified=1&category=105793&platform=&variable40520=&emulator=0&video=&obsolete=&date='
# All Icons, WM
rtdxENGiconsWM = 'https://www.speedrun.com/ajax_leaderboard.php?variable40519=138361&game=pmddx&verified=1&category=105888&platform=&variable40520=&emulator=0&video=&obsolete=&date='
# All Icons, No WM
rtdxENGiconsNW = 'https://www.speedrun.com/ajax_leaderboard.php?variable40519=138362&game=pmddx&verified=1&category=105888&platform=&variable40520=&emulator=0&video=&obsolete=&date='

# PMD Series Any% Unrestricted
pmdseriesAnyUR = 'https://www.speedrun.com/ajax_leaderboard.php?game=multiplemysterydungeon&verified=1&category=52548&platform=&emulator=2&video=&obsolete=&date='
# PMD Series Any% No WM No QS
pmdseriesAnySS = 'https://www.speedrun.com/ajax_leaderboard.php?game=multiplemysterydungeon&verified=1&category=99524&platform=&emulator=2&video=&obsolete=&date='
# PMD Series Recruit Em All Unrestricted
pmdseriesREAUR = 'https://www.speedrun.com/ajax_leaderboard.php?game=multiplemysterydungeon&verified=1&category=104076&platform=&emulator=2&video=&obsolete=&date='

RTList = [['Any% ENG', 'Unrestricted', rtENGanyUR], ['Any% ENG', 'No WM', rtENGanyNW], ['Any% ENG', 'No WM No QS', rtENGanySS], ['Any% JPN', 'Unrestricted', rtJPNanyUR], ['Any% JPN', 'No WM', rtJPNanyNW], ['Any% JPN', 'No WM No QS', rtJPNanySS], ['All Icons', 'Unrestricted', rtENGiconsUR], ['All Icons', 'No WM', rtENGiconsNW], ['All Icons', 'No WM No QS', rtENGiconsSS], ['Recruit Em All', 'Unrestricted', rtENGreaUR], ['Recruit Em All', 'No WM', rtENGreaNW], ['Recruit Em All', 'No WM No QS', rtENGreaSS], ['Low%', 'Unrestricted', rtENGlowUR], ['All Dungeons', 'No WM No QS', rtENGadSS]]
TDList = [['Any% ENG', 'with WM', tdENGanyWM], ['Any% ENG', 'No WM', tdENGanyNW], ['Any% JPN', 'with WM', tdJPNanyWM], ['Any% JPN', 'No WM', tdJPNanyNW], ['Beat Darkrai', 'with WM', tdENGdarkWM], ['Beat Darkrai', 'No WM', tdENGdarkNW], ['Recruit Em All', 'Unlimited WM', tdENGreaUW], ['Recruit Em All', 'Minimum WM', tdENGreaMW]]
SkyList = [['Any% ENG', 'with WM', skyENGanyWM], ['Any% ENG', 'No WM', skyENGanyNW], ['Any% JPN', 'with WM', skyJPNanyWM], ['Any% JPN', 'No WM', skyJPNanyNW], ['Beat Darkrai ENG', 'with WM', skyENGdarkWM], ['Beat Darkrai ENG', 'No WM', skyENGdarkNW], ['Beat Darkrai JPN', 'with WM', skyJPNdarkWM], ['Beat Darkrai JPN', 'No WM', skyJPNdarkNW], ['Recruit Em All', 'with WM', skyENGreaWM], ['Recruit Em All', 'No WM', skyENGreaNW], ['All Icons', 'with WM', skyENGiconsWM], ['All Icons', 'No WM', skyENGiconsNW], ['All Special Episodes', '', skyENGase]]
WiiList = [['Any%', '', wiiJPNany]]
GatesList = [['Any% ENG', 'with WM', gtiENGanyWM], ['Any% ENG', 'No WM', gtiENGanyNW], ['Any% JPN', 'with WM', gtiJPNanyWM], ['Any% JPN', 'No WM', gtiJPNanyNW], ['Recruit Em All', 'with WM', gtiENGreaWM], ['Recruit Em All', 'No WM', gtiENGreaNW]]
SuperList = [['Any% ENG', 'with WM', smdENGanyWM], ['Any% ENG', 'No WM', smdENGanyNW], ['Any% JPN', 'with WM', smdJPNanyWM], ['Any% JPN', 'No WM', smdJPNanyNW], ['100%', 'with WM', smdENG100WM]]
RTDXList = [['Any% ENG', 'with WM', rtdxENGanyWM], ['Any% ENG', 'No WM', rtdxENGanyNW], ['Any% JPN', 'with WM', rtdxJPNanyWM], ['Any% JPN', 'No WM', rtdxJPNanyNW], ['All Icons', 'with WM', rtdxENGiconsWM], ['All Icons', 'No WM', rtdxENGiconsNW]]
SeriesList = [['PMD Series Any%', 'Unrestricted', pmdseriesAnyUR], ['PMD Series Any%', 'No WM No QS', pmdseriesAnySS], ['PMD Series Recruit Em All', 'Unrestricted', pmdseriesREAUR]]
CombinedList = [RTList, TDList, SkyList, WiiList, GatesList, SuperList, RTDXList, SeriesList]
GameNames = ["Red/Blue Rescue Team", "Explorers of Time/Darkness", "Explorers of Sky", "WiiWare", "Gates to Infinity", "Super Mystery Dungeon", "Rescue Team DX", "Multiple Mystery Dungeon Games"]

driver = webdriver.Chrome()
myDB = sqlite3.connect('./db.sqlite3')
counter = 0


for runList in CombinedList:
	#print game name
	print(GameNames[counter])
	for run in runList:
		# print run category
		printLine = run[0] + " " + run[1] + ': '
		# access run at url
		driver.get(run[2])
		soup = BeautifulSoup(driver.page_source, "html.parser")
		runtime = ''
		runnerSlice = ''
		try:
			runtime = soup.find('td', class_='nobr center hidden-xs').get_text()
			runnerName = soup.find('a', class_='link-username nobr nounderline').get_text()
			# slice names because sr.c stores the name twice
			sliceIndex = int(len(runnerName)/2)
			runnerSlice = runnerName[:sliceIndex]
			print(run[0] + " " + run[1] + " " + runnerSlice + " " + runtime)
		except:
			print("No data exists for this game/category/rule combination")
	
		# print run time
		
		# write run time and runner name to database
		myDB.execute("UPDATE records_run SET playerName=:pname, runTime=:rTime WHERE game=:game AND category=:cat AND ruleset=:rSet", {"pname": runnerSlice, "rTime": runtime, "game": GameNames[counter], "cat": run[0], "rSet": run[1]})
		myDB.commit()
		
	counter += 1
	print()

myDB.close()
driver.close()

