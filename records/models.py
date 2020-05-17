from django.db import models

# Create your models here.
class Run(models.Model):
	# Base game name
	game = models.CharField(max_length=200, help_text='Name of the game name (including Multiple)')
	# Category name
	category = models.CharField(max_length=200, help_text='Name of the category (ie. any%, Recruit Em All)')
	# Ruleset (WM/No WM etc.)
	ruleset = models.CharField(max_length=200, help_text='Name of applicable rulesets ie. if Wonder Mail is permitted')
	# Runner name
	playerName = models.CharField(max_length=200, help_text='sr.c username of runner')
	# Time (formatted as a string)
	runTime = models.CharField(max_length=200, help_text='Format: *h *m *s')
	
	def __str__(self):
		return f'{self.game} {self.category} {self.ruleset}'
