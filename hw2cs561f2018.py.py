'''
Helper function converts string to bool
'''
def getBool(val):
	#returns False if string is N,n or 0
	if val == 'N' or val == 'n' or val == '0':
		return False
	#returns True if string is Y,y or 1
	elif val =='Y' or val == 'y' or val == '1':
		return True
	#rise exception because the value passes is invalid
	raise ValueError

'''
Converts string to dict
'''
def getApplicant(line):
	applicant = {}
	#first 5 chars is applicant id
	applicant['id'] = line[0:5]
	#next char i.e 5th is Gender
	applicant['gender'] = line[5]
	#next 3 chars store the age
	applicant['age'] = int(line[6:9])
	#next char is Y/N for pets
	applicant['pets'] = getBool(line[9])
	#next char is Y/N for medical condition
	applicant['medical'] = getBool(line[10])
	#next char is Y/N for car
	applicant['car'] = getBool(line[11])
	#next char is Y/N for driving license
	applicant['drivingLicense'] = getBool(line[12])
	#next 7 chars 0/1 are for each day of week
	applicant['dayOfWeek'] = []
	for i in range(7):
		applicant['dayOfWeek'].append(getBool(line[13+i]))
	return applicant

'''
Returns the index of allApplicants at which applicantId is present
'''
def getIndex(allApplicants,applicantId):
	for i in range(len(allApplicants)):
		if allApplicants[i]['id'] == applicantId:
			return i
'''
Removes each occurence of applicantId in selected list
from allApplicants list
'''
def remove_already_selected(allApplicants,selected):
	for applicantId in selected:
		del allApplicants[getIndex(allApplicants,applicantId)]
'''
Checks for SPLA eligibility constraints from allApplicants
i.e has Car, driving license but no medical condition
'''
def getAllEligibleSPLA(allApplicants):
	eligibleApplicants = []
	for applicant in allApplicants:
		if applicant['car'] and applicant['drivingLicense'] and not applicant['medical']:
			eligibleApplicants.append(applicant)
	return eligibleApplicants
'''
Checks for SPLA eligibility constraints from allApplicants
i.e age > 17,is female and without pets
'''
def getAllEligibleLHSA(allApplicants):
	eligibleApplicants = []
	for applicant in allApplicants:
		if applicant['age'] > 17 and applicant['gender'] == 'F' and not applicant['pets']:
			eligibleApplicants.append(applicant)
	return eligibleApplicants
'''
Returns a list of applicants dict
that are present in both the lists
'''
def getCommon(applicantsA,applicantsB):
	commonApplicants = []
	for applicantA in applicantsA:
		for applicantB in applicantsB:
			if applicantA['id'] == applicantB['id']:
				commonApplicants.append(applicantA)
	return commonApplicants
'''
Calculates the total occupancy of SPLA 
due to the already selected applicants
'''
def getOccupancy(allApplicants,selectedSPLA):
	occupancy = {}
	for applicantId in selectedSPLA:
		index = getIndex(allApplicants,applicantId)
		for i in range(len(allApplicants[index]['dayOfWeek'])):
			if i not in occupancy.keys():
				occupancy[i] = 0
			if allApplicants[index]['dayOfWeek'][i]:
				occupancy[i] += 1
	return occupancy
'''
Gives score to applicant based on the changes occupancy 
of the SPLA
#if for any day of the week the occupancy is over 10
return -1
'''
def getScore(occupancy,dayOfWeek,parkingLotSize):
	totalVal = 0
	for i in range(len(dayOfWeek)):
		if dayOfWeek[i] + occupancy[i] > parkingLotSize:
			return -1
		else:
			totalVal += (dayOfWeek[i] + occupancy[i])
	return totalVal
'''
returns the applicantId which has highest score 
when selected by SPLA
'''
def selectBest(targetApplicants,occupancy,parkingLotSize):
	bestApplicantId = None
	maxScore = 0
	for applicant in targetApplicants:
		score = getScore(occupancy,applicant['dayOfWeek'],parkingLotSize)
		if maxScore < score:
			maxScore = score
			bestApplicantId = applicant['id']
	return bestApplicantId
'''
Reads the data from the filename
and returns 3 lists
allApplicants =- list of dict containing info of all applicants
applicantIdLHSA =- list of applicantId's already selected by LHSA
applicantIdSPLA =- list of applicantId's already selected by SPLA
'''
def readDataFromFile(filename):
	with open(filename,'r') as file:
		b = int(file.readline().strip())
		p = int(file.readline().strip())
		l = int(file.readline().strip())
		applicantIdLHSA = []
		for i in range(l):
			applicantIdLHSA.append(file.readline().strip())
		s = int(file.readline().strip())
		applicantIdSPLA = []
		for i in range(s):
			applicantIdSPLA.append(file.readline().strip())
		a = int(file.readline().strip())
		allApplicants = []
		for i in range(a):
			applicant = getApplicant(file.readline().strip())
			allApplicants.append(applicant)
	return allApplicants,applicantIdSPLA,applicantIdLHSA,p


def main():
	allApplicants,applicantIdSPLA,applicantIdLHSA,parkingLotSize = readDataFromFile('input25.txt')

	occupancy = getOccupancy(allApplicants,applicantIdSPLA)
	remove_already_selected(allApplicants,applicantIdLHSA)
	remove_already_selected(allApplicants,applicantIdSPLA)


	eligibleSPLA = getAllEligibleSPLA(allApplicants)
	eligibleLHSA = getAllEligibleLHSA(allApplicants)
	commonEligible = getCommon(eligibleSPLA,eligibleLHSA)
	targetApplicants = []
	if len(commonEligible) == 0:
		targetApplicants = eligibleSPLA
	else:
		targetApplicants = commonEligible
	with open('output.txt','w') as file:
		file.write(selectBest(targetApplicants,occupancy,parkingLotSize))

main()