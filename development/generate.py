###########################################################################################	
###########################################################################################	
###########################################################################################
def Scenario(p):
	#from math import *
	from random import randint
	from random import choice

	# Create empty lists
	profPeriod = []
	profSubject = []
	sbjPeriod = []
	sbjHPW = []
	sbjOrdered = []
	sbjGroups = []
	sbjProfs = []
	groupsHPW = []
	# Create a list to keep record of subjects that are taught by more than one professor
	repeating = []
	for i in range(p*2):
		repeating.append(0) # the list starts filled by zeros as no professor is known to be teaching any of the subjects until now

	for i in range(p): # Professors preferences

		# Periods
		morning = randint(1,2) # 1 represents that the professor doesn't prefer this period, 2 represents the professor prefers the period
		afternoon = randint(1,2)
		night = randint(1,2)
		if(morning==afternoon==night): morning,afternoon,night = 2,2,2
		prefs = (morning,afternoon,night)
		profPeriod.append(prefs) # store this professor's preferences about class periods
		if(prefs==(2,1,1)):
			period_message = ('and prefers teaching in the morning only.')
		elif(prefs==(1,2,1)):
			period_message = ('and prefers teaching in the afternoon only.')
		elif(prefs==(1,1,2)):
			period_message = ('and prefers teaching in the evening only.')
		elif(prefs==(2,2,1)):
			period_message = ('and prefers teaching in the morning and afternoon.')
		elif(prefs==(2,1,2)):
			period_message = ('and prefers teaching in the morning and evening.')
		elif(prefs==(1,2,2)):
			period_message = ('and prefers teaching in the afternoon and evening.')
		else:
			period_message = ("and doesn't have preferences for teaching in a specific period.")
		

		# Subjects
		_list = list(range(p*2)) # There will exist 2 times more subjects than professors
		# Each professor will be able to teach 4 subjects, sbj0 is the preferred subject, sbj3 is the less preferred one
		sbj0 = choice(_list)
		_list.remove(sbj0)
		repeating[sbj0] += 1
		sbj1 = choice(_list)
		_list.remove(sbj1)
		repeating[sbj1] += 1
		sbj2 = choice(_list)
		_list.remove(sbj2)
		repeating[sbj2] += 1
		sbj3 = choice(_list)
		repeating[sbj3] += 1
		prefs = [sbj0,sbj1,sbj2,sbj3]
		profSubject.append(prefs) # store this professor's preferences about subject teaching
		
		#print('Professor %i is able to teach the following subjects, in order of preference: subject %i, subject %i, subject %i and subject %i;' % (i,sbj0,sbj1,sbj2,sbj3),period_message)

	for i in range(len(repeating)): # Order subjects in decrescent sequence based on the number of professors that are able to teach the subject
		m = max(repeating)
		if(m==0): break
		else:
			pos = [k for k, x in enumerate(repeating) if x == m] # as the "repeating" list is parallel to the subjects list, the position of an element in "repeating" indicates the subject number
			for j in range(len(pos)):
				sbjOrdered.append(pos[j]) # store the subjects into sbjOrdered in decreasing order
				repeating[pos[j]] = 0	
	print('\n')

	for i in range(p*2): # Subjects info

		# Period
		period = choice([1,1,1,2]) # 1 represents morning and night, 2, afternoon. 75% of chances for 1 and 25% for 2
		sbjPeriod.append(period) # store the period that this subject is offered
		if(period==1):
			offered_message = 'morning and evening.'
		else:
			offered_message = 'afternoon.'

		# Hours per Week (hpw)
		if(period==1): _list = [2,2,3,3,3,4,4,4,4,5] # subjects in period "1" can range from 2 to 5 hours per week. 40% of chances for 4, 30% for 3, 20% for 2 and 10% for 5
		else: _list = [2,2,3,4] # subjects in period "2" can range from 2 to 4 hours per week. 50% of chances for 2, 25% for 3 and 25% for 4
		hpw = choice(_list)
		sbjHPW.append(hpw) # store the hours per week that this subject will have
		
		#print("Subject %i has %i hours per week and is offered in the" % (i,hpw),offered_message)

	# Groups of subjects that need to be offered in a way that one can attend all the subjects in that group
	num_groups = int(len(sbjOrdered)/20) # the number will be defined by the number of subjects that are able to be offered divided by 20
	count = 0
	while(num_groups > 0):
		group = []
		for i in range(5): # each group will be composed by 5 subjects b-a+1 = 5
			mod = i+5*count
			group.append(sbjOrdered[mod])
		count += 1
		num_groups -= 1
		sbjGroups.append(group)

	# Ensure that any of the subject groups exceed 20 hours per week in a single period
	rerun = 0
	for i in range(len(sbjGroups)):
		totalHPW_1 = 0
		totalHPW_2 = 0
		for j in range(5):
			period = sbjPeriod[sbjGroups[i][j]]
			if(period==1):
				totalHPW_1 += sbjHPW[sbjGroups[i][j]]
			else:
				totalHPW_2 += sbjHPW[sbjGroups[i][j]]
		if(totalHPW_1>20): rerun = 1
		else: pass
		if(totalHPW_2>20): rerun = 1
		else: pass

	# Get professors that can teach each subject
	for h in range(len(sbjGroups)): # do this for all the groups
		for i in range(5): # four subjects in each group
			subject = sbjGroups[h][i] # Obtain subject
			professors=[]
			for j in range(4): # each professor may teach 4 subjects
				for k in range(len(profSubject)):
					if(profSubject[k][j]==subject): # check if the professor teaches this subject
						professors.append((k,j)) # if so, get the professor number and the priority this professor gives for this discipline
					else: pass
			sbjProfs.append(professors) # register the professors as candidates for teaching this subject

	if(rerun==1): Scenario(p)
	else: pass

	return profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs
