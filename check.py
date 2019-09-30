import math

# Value used to find if potential scores are legitimate or not (e.g. 79.2 is not but 79.002 is)
MIN_DIF = 1e-04
MINSCORE = 0

""" Function intends to find the number of subjects released and its corresponding marks once WAM is updated """
def find_marks_subjs(wam, totalScore, totalSubjs):
	highestScore = 99

	# On the basis that a person takes between 1 to 6 subjects in current term
	for subjsTaken in range(1, 7):
		estimatedScore = (wam * (totalSubjs + subjsTaken) - totalScore)
		if (MINSCORE <= estimatedScore <= highestScore):
			# To check if estimatedScore value is close to an integer 
			if math.isclose(estimatedScore, int(estimatedScore), rel_tol = MIN_DIF):
				return (int(estimatedScore), subjsTaken)
		highestScore += 100
	return None
