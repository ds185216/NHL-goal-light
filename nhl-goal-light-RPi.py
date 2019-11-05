from urllib.request import urlopen
import json
import time
import RPi.GPIO as GPIO

def read_team():
	global team_name
	team_name = open('team.txt', 'r').read()[:-1]

def write_team():
	global team_name
	team_name = 'redwings'
	f = open('team.txt', 'w')
	f.write(str(team_name))

def read_delay():
	global delay
	delay = int(open('delay.txt', 'r').read())

def write_delay():
	global delay
	delay = 5
	f = open('delay.txt', 'w')
	f.write(str(delay))

def score_check(home_away_score):
	global score, game, refresh, delay, led
	if game[home_away_score] != "":
		if int(game[home_away_score]) > score:
			time.sleep(delay)
			GPIO.setup(led, GPIO.OUT)
			GPIO.output(led, 1)
			GPIO.output(led, 0)
			GPIO.cleanup()
			score = int(game[home_away_score])
			refresh = normal_refresh - delay
		else:
			score = int(game[home_away_score])

try:
	read_delay()
except:
	write_delay()
try:
	read_team()
except:
	write_team()

normal_refresh = 5
score_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?'
score = 0

#pinout
led = 23
GPIO.setmode(GPIO.BOARD)

scoreboard = json.loads(urlopen(score_url).read().decode('utf-8').replace("loadScoreboard(","").replace(")",""))['games']
for game in scoreboard:
	if game['atv'] == team_name and game['bs'] == 'LIVE':
		score = int(game['ats'])
	if game['htv'] == team_name and game['bs'] == 'LIVE':
		score = int(game['hts'])

while 1:
	refresh = normal_refresh
	scoreboard = json.loads(urlopen(score_url).read().decode('utf-8').replace("loadScoreboard(","").replace(")",""))['games']
	for game in scoreboard:
		if game['atv'] == team_name and game['bs'] == 'LIVE':
			score_check('ats')
		if game['htv'] == team_name and game['bs'] == 'LIVE':
			score_check('hts')
	time.sleep(refresh)