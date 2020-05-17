from django.shortcuts import render
from records.models import Run

import sqlite3
import os

# Create your views here.
def index(request):
	
	num_categories = Run.objects.all().count()
	num_valid_categories = Run.objects.exclude(playerName="").count()
	# list containing all distinct entries in the "game" column
	# Manually collected for now
	myDB = sqlite3.connect('./db.sqlite3')
	# see StackOverflow "sqlite3 fetchall to list"
	myDB.row_factory = lambda cursor, row: row[0]
	list_of_games = myDB.execute("SELECT DISTINCT game FROM records_run").fetchall()
	myDB.close()
	
	valid_runs = Run.objects.exclude(playerName="")
	all_runs = Run.objects.all()
	
	context = {
		'num_categories': num_categories,
		'num_valid_categories': num_valid_categories,
		'list_of_games': list_of_games,
		'all_runs': all_runs
		
	}
	
	return render(request, 'index.html', context=context)
