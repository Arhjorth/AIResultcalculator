from os import listdir
import math
from decimal import *
import sys

def calculateActionScore(ourScore, bestScore):
	return (bestScore/ourScore)# if (bestScore/ourScore) <= 1 else 1

def calculateTimeScore(ourTime, bestTime):
	return math.log(bestTime)/math.log(ourTime)# if math.log(bestTime)/math.log(ourTime) <= 1 else 1


def round(x,d):
	if d == 3 :
		return float(Decimal(x).quantize(Decimal('0.000'), rounding = ROUND_HALF_UP))
	if d == 2:
		return Decimal(x).quantize(Decimal('0.00'), rounding = ROUND_UP)


def toLatex(ourActions, ourTime, actionResult, timeResult, bestActions, bestTime):
	for k,v in ourActions.items():
		if v == 0:
			v = "No solution found"
			#print(k+ ".lvl & ", v , "\\\\")
		else:
			print(k + " &", v,"&", actionResult[k] ,"&", ourTime[k] / 1000, "&", timeResult[k] , "\\\\")



def calculateScores(MAourTimes, MAourActions, SAourTimes, SAourActions):

	# MA Actions

	MAkeys = ["MAAIoliMAsh", "MABeliebers", "MABlinky", "MABoxBunny", "MABronies", "MADAT", "MADoDo", "MAEvilCorp", "MAFooBar", "MAGeneralAI", "MAgroupname", "MAGroupOne", "MAHiveMind", "MAIamGreedy", "MAJomarki", "MAKalle", "MALemmings", "MALiquorice", "MAMasAiArne", "MAMASters", "MANeverMind", "MAOmnics", "MAtnrbt"]
	MABestActionValues = [80, 99, 52, 842, 214, 231, 4, 192, 12, 128, 32, 1004, 107, 188, 41, 31, 53, 69, 1563, 214, 27, 579, 1108]
	MABestTimeValues =  [281, 385, 46, 902, 530, 216, 15, 253, 106, 265, 104, 700, 264, 1168, 71, 128, 71, 151, 2073, 526, 114, 658, 1714]
	MABestActions = dict(zip(MAkeys,MABestActionValues))
	MABestTime = dict(zip(MAkeys, MABestTimeValues))

	SAkeys = ["SAAIoliMAsh", "SABeliebers", "SABlinky", "SABoxBunny", "SABronies", "SADAT", "SADoDo", "SAEvilCorp", "SAFooBar", "SAGeneralAI", "SAgroupname", "SAHALnineK", "SAHiveMind", "SAIamGreedy", "SAJomarki", "SAKalle", "SALemmings", "SALiquorice", "SAMasAiArne", "SAMASters", "SANeverMind", "SAOmnics", "SATALK", "SAtnrbts"]
	SABestActionValues = [1930, 316, 124, 3213, 12662, 953, 228, 3262, 193, 521, 3687, 100, 234, 927, 60, 202, 114, 95, 604, 212, 238, 3592, 239, 262]
	SABestTimeValues = [1416, 252, 17, 1054, 1830, 484, 122, 5970, 3341, 287, 433, 3955, 269, 608, 15, 152, 118, 80, 203, 268, 182, 2307, 142, 205]
	SABestActions = dict(zip(SAkeys,SABestActionValues))
	SABestTime = dict(zip(SAkeys,SABestTimeValues))


	MAActionResult = {}
	MATimeResult =  {}

	SAActionResult = {}
	SATimeResult = {}


	for c in MAkeys:

		MATimeResult[c] = round(calculateTimeScore(MAourTimes[c],MABestTime[c]),3) if MAourTimes.get(c) else 0
		MAActionResult[c] = round(calculateActionScore(MAourActions[c], MABestActions[c]),3)  if MAourActions.get(c) else 0

	for c in SAkeys:
		SATimeResult[c] = round(calculateTimeScore(SAourTimes[c],SABestTime[c]),3)  if SAourTimes.get(c) else 0
		SAActionResult[c] = round(calculateActionScore(SAourActions[c], SABestActions[c]),3)  if SAourActions.get(c) else 0

	SAActionSum = round(sum(SAActionResult.values()), 3)
	print("SAActionResults: ",SAActionResult, "TOTAL SCORE: ", SAActionSum)
	SATimeSum = round(sum(SATimeResult.values()), 3)
	print("SATimeResults: ",SATimeResult, "TOTAL SCORE: ", SATimeSum)

	MAActionSum = round(sum(MAActionResult.values()), 3)
	print("MAActionResults: ",MAActionResult, "TOTAL SCORE: ", MAActionSum)
	MATimeSum = round(sum(MATimeResult.values()), 3)
	print("MATimeResults: ",MATimeResult, "TOTAL SCORE: ", MATimeSum)

	print("\n\nTOTAL SCORE IN ALL CATEGORIES: ", round(SAActionSum + SATimeSum +  MAActionSum+ MATimeSum,2))

	toLatex(SAourActions, SAourTimes, SAActionResult, SATimeResult, SABestActions, SABestTime)
	toLatex(MAourActions, MAourTimes, MAActionResult, MATimeResult, MABestActions, MABestTime)


def	run(dir):


	MAourTimes = {}
	MAourActions = {}
	SAourTimes = {}
	SAourActions = {}

	completedlvls = 0
	levelsInTotal = 0
	MAlvlsCompleted = 0
	SAlvlsCompleted = 0

	for fileno ,f in enumerate(listdir(dir)):
		levelsInTotal = fileno
		successLine = - 1
		success = False
		timeScore = -1
		actionScore = -1
		with open(dir + "\\" + f,'r') as file:
			for lineno, line in enumerate(file):
				if line == "successful\n":
					successLine = lineno
					success = True
					completedlvls+=1
				if success:
					if lineno == successLine + 1:
						timeScore = int(line)
					elif lineno == successLine + 2: # Number of joint actions is on the second line beneath the successfull tag
						actionScore = int(line)
		if success:
			if f[0:2] == "MA":
				MAlvlsCompleted += 1
				MAourTimes[f[:-4]] = timeScore
				MAourActions[f[:-4]] = actionScore
			else:
				SAlvlsCompleted += 1
				SAourTimes[f[:-4]] = timeScore
				SAourActions[f[:-4]] = actionScore
		elif success == False:
			if f[0:2] == "MA":
				MAourTimes[f[:-4]] = 0
				MAourActions[f[:-4]] = 0
			else:
				SAourTimes[f[:-4]] = 0
				SAourActions[f[:-4]] = 0

	calculateScores(MAourTimes, MAourActions, SAourTimes, SAourActions)

	print("\n\nLevels in total:", levelsInTotal, ", succesful:", completedlvls, "\n", "Completed MAlvls:", MAlvlsCompleted, "\n", "Completed SAlvls:", SAlvlsCompleted  )


dir = "C:\\Users\\arhjo\\Desktop\\MASters\\SingleRun"
#dir = input("Please enter path here: ")
run(dir)
