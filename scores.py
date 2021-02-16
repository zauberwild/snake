"""
This script handles saving the highscores.
You will be able to type in your name, 
and it will be saved with your score
"""
from pathlib import Path
gen_path = str(Path(__file__).parent.absolute())
pathToFile = gen_path + "/lib/scores"

names = []		# this list will hold all the names
scores	= []	# this list will hold all the scores


def loadScores():
	"""
	This function should be called once in the beginning
	to load preexistent scores into a lists
	"""
	file_obj = open(pathToFile,"r")

	if file_obj.mode == 'r':					# check if file is readable
		file_list = file_obj.readlines()		# load all lines in a list
		for i in file_list:
			j = i.split(',')					# split list up
			names.append(j[0])					# and save it
			scores.append(int(j[1]))
	
	file_obj.close()

def getScoreByName(name):
	""" 
	This function will search for the name and
	will, if found, return the scores
	"""
	for idx, val in enumerate(names):
		if val == name:
			return scores[idx]

def getHighscore():
	""" 
	returns the highest score
	"""
	max_val = -1
	max_idx = -1
	if len(scores) > 0:
		for idx, val in enumerate(scores):		# check every entry
			if val > max_val:		# if new max, then save
				max_val = val
				max_idx = idx
		return names[max_idx], max_val		# return the final max
	else:
		return None, None					# retrun none if list is empty

def addScore(name, score):
	""" 
	adds a new score to the list
	"""
	a_idx = -1
	for idx, val in enumerate(names):		# check if name already exists
		if val == name:
			a_idx = idx
	
	if a_idx == -1:							# if it doesn't, simply add it
		names.append(name)
		scores.append(score)
	else:									# otherwise replace the old score with the new one
		scores[a_idx] = score
	
	__saveScores__()

def __saveScores__():
	""" 
	will save all scores into the file defined by 'pathToFile'
	"""
	file_obj = open(pathToFile,'w')
	file_obj.truncate(0)				# clear file
	for idx, val in enumerate(names):
		line = names[idx] + "," + str(scores[idx])		# generate line
		if idx < len(names) - 1:						# add \n-signal for every but the last line
			line += "\n"
		file_obj.write(line)							# finally write the file
	
	file_obj.close()


if False: # example code here
	loadScores()

	na = "Schiemann"
	sc = getScoreByName(na)
	print("score of " + na + ": " + str(sc))

	print("###")

	hs = getHighscore()
	print(hs)

	print("###")
	for idx, val in enumerate(names):
		print(val + ":" + str(scores[idx]))

	n_na = "Niko"
	n_sc = 49
	addScore(n_na, n_sc)

	print("#")

	for idx, val in enumerate(names):
		print(val + ":" + str(scores[idx]))
