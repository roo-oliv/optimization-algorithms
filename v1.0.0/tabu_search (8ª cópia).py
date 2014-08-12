# Modules importing
from math import *
from random import randint
from random import choice
import copy
import time

###########################################################################################
def scenario(p):
	# Declare global variables
	global profPeriod
	global profSubject
	global sbjPeriod
	global sbjHPW
	global sbjOrdered
	global sbjGroups
	global sbjProfs
	global report
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
		
		print('Professor %i is able to teach the following subjects, in order of preference: subject %i, subject %i, subject %i and subject %i;' % (i,sbj0,sbj1,sbj2,sbj3),period_message)

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
		
		print("Subject %i has %i hours per week and is offered in the" % (i,hpw),offered_message)

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

	if(rerun==1): scenario(p)
	else: pass

	return
	
###########################################################################################
def getReport(p):
	# Write report
	report = "\nThere are %(prof_num)d professors in the university and %(total_sbj_num)d subjects that can be offered in this course.\n\n %(groups_num)d groups of subjects were choosen to be offered at this time, each subject group is composed by 5 subjects that are supposed to be attended simultaneously by students that are supposed to attend that group. %(grouped_sbj_num)d subjects will be offered inside subject groups, other %(free_sbj_num)d subjects will be offered independently. So %(offered_sbj_num)d out of the universe of %(total_sbj_num)d subjects will be offered this time.\n\n" % \
		{"prof_num":p,"total_sbj_num":p*2,"groups_num":len(sbjGroups),"grouped_sbj_num":5*len(sbjGroups),"free_sbj_num":len(sbjBook)-5*len(sbjGroups),"offered_sbj_num":len(sbjBook)}
		
	return report

###########################################################################################
def getProf(sbj,candidates,period):
	global profPos
	global force

	got = 0
	while(got==0):
		if(len(candOrdered)==profPos): profPos = 0; force = 1
		else: pass
		if(profPeriod[candOrdered[profPos][1]][period-1]==2 or force==1):
			period += 1
			professor = candOrdered[profPos][1]
			got = 1
		else:
			profPos += 1

	return professor

###########################################################################################
def assign(p):
	# Declare global variables
	global candOrdered
	global sbjBook
	global profBook
	global profSche
	global errors
	global profPos
	global force
	global sbjSche
	# Create empty lists and dictionaries
	candOrdered = []
	sbjBook = {}
	profBook = {}
	sbjSche = []
	
	print('\n')
	
	for i in range(p*2):
		sbjSche.append([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])

	for i in range(len(sbjGroups)): # iterate for all subject groups
		slots = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
		for j in range(5): # each group is composed by 5 subjects
			sbj = sbjGroups[i][j] # obtain the current subject number
			candidates = list(candAval[j+5*i])
			candOrdered = sorted(candidates, key=lambda item: item[0], reverse=True)
			hpw = sbjHPW[sbj] # get the hours per week for this subject
			period = sbjPeriod[sbj]
			profPos = 0
			force = 0

			# mod -> 0: just one period; 1: morning and night
			if(period==1): repeat = 1
			else: repeat = 0
			while(repeat>=0):
				alloc = 0
				alloc2 = 0
				alloc3 = 0
				a = 0
				b = 0
				c = 0
				waste = 0
				c_mod = 0
				if(repeat==1 and period==1): period = 3
				else: pass
				# Get the slots that will be occupied
				t = 0
				if(hpw==2):
					while(alloc==0):
						if(slots[period-1][a]==0):
							slot = a
							slots[period-1][a] += 2
							alloc = 1
						else:
							a += 1
						if(a==10):
							alloc = -1
						else: pass
					if(alloc==-1):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
						errors += 1
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor = getProf(sbj,candidates,period)
							gotProf = gotProf
							info = [sbj,period,hpw,professor,i,slot]
							if(profSche[professor][period-1][slot]==0):
								profSche[professor][period-1][slot] += 2
								sbjSche[sbj][period-1][slot] += 2
								gotProf = 1
							else: profPos += 1
							if(t>len(candidates)**2): gotProf = -1; print('Fatal error: No professors available at all!')
				elif(hpw==3):
					while(alloc==0):
						if(slots[period-1][a]==0):
							slot = a
							slots[period-1][a] += 2
							alloc = 1
						else:
							a += 1
						if(a==10):
							alloc = -1
						else: pass
					control = 0
					while(alloc2==0):
						if(a%2==0): mod = 1
						else: mod = -1
						if(control==0):
							for k in range(4,-1,-1):
								if(9>=a+k+mod>=0 and k+mod!=0):
									b = a+k+mod
									break
							else: alloc2 = -1
						else: pass
						if(slots[period-1][b]==1 and waste==0):
							slot2 = b
							slots[period-1][b] += 1
							alloc2 = 1
						elif(slots[period-1][b]==0 and waste==1):
							slot2 = b
							slots[period-1][b] += 1
							alloc2 = 1
						else:
							control += 1
							if(control%2==1 and b-control!=a):
								b -= control
								if(b<0 and b+1+control!=a): control += 1; b += control
							elif(b+control!=a):
								b += control
								if(b>9 and b-1-control!=a): control += 1; b -= control
							else: pass
							if(waste==0 and not(0<=b<=9) and a!=5):
								b = 5
								control = 0
								waste = 1
							elif(waste==1 and not(0<=b<=9)):
								alloc2 = -1
								print('ALLOC ERROR 1 in alloc2, ',hpw,period,'\n',slots)
							else: pass
					if(alloc==-1 or alloc2==-1):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
						errors += 1
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor = getProf(sbj,candidates,period)
							gotProf = gotProf
							info = [sbj,period,hpw,professor,i,slot,slot2]
							if(profSche[professor][period-1][slot]==0 and profSche[professor][period-1][slot2]<2):
								profSche[professor][period-1][slot] += 2
								profSche[professor][period-1][slot2] += 1
								sbjSche[sbj][period-1][slot] += 2
								sbjSche[sbj][period-1][slot2] += 1
								gotProf = 1
							else: profPos += 1
							if(t>len(candidates)**2): gotProf = -1; print('Fatal error: No professors available at all!')
				elif(hpw==4):
					while(alloc==0):
						if(slots[period-1][a]==0):
							slot = a
							slots[period-1][a] += 2
							alloc = 1
						else:
							a += 1
						if(a==10):
							alloc = -1
						else: pass
					control = 0
					while(alloc2==0):
						if(a%2==0): mod = 1
						else: mod = -1
						if(control==0):
							for k in range(4,-1,-1):
								if(9>=a+k+mod>=0 and k+mod!=0):
									b = a+k+mod
									break
							else: alloc = -1
						else: pass
						if(slots[period-1][b]==0):
							slot2 = b
							slots[period-1][b] += 2
							alloc2 = 1
						else:
							control += 1
							if(control%2==1 and b-control!=a):
								b -= control
								if(b<0 and b+1+control!=a): control += 1; b += control
							elif(b+control!=a):
								b += control
								if(b>9 and b-1-control!=a): control += 1; b -= control
							else: pass
							if(waste==0 and not(0<=b<=9) and a!=5):
								b = 5
								control = 0
								waste = 1
							elif(waste==1 and not(0<=b<=9)):
								alloc2 = -1
					if(alloc==-1 or alloc2==-1):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
						errors += 1
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor = getProf(sbj,candidates,period)
							gotProf = gotProf
							info = [sbj,period,hpw,professor,i,slot,slot2]
							if(profSche[professor][period-1][slot]==0 and profSche[professor][period-1][slot2]==0):
								profSche[professor][period-1][slot] += 2
								profSche[professor][period-1][slot2] += 2
								sbjSche[sbj][period-1][slot] += 2
								sbjSche[sbj][period-1][slot2] += 2
								gotProf = 1
							else: profPos += 1
							if(t>len(candidates)**2): gotProf = -1; print('Fatal error: No professors available at all!')
				else:
					while(alloc==0):
						if(slots[period-1][a]==0):
							slot = a
							slots[period-1][a] += 2
							alloc = 1
						else:
							a += 1
						if(a==10):
							alloc = -1
						else: pass
					control = 0
					while(alloc2==0):
						if(a%2==0): mod = 1
						else: mod = -1
						if(control==0):
							for k in range(4,-1,-1):
								if(9>=a+k+mod>=0 and k+mod!=0):
									b = a+k+mod
									break
							else: alloc2 = -1
						else: pass
						if(slots[period-1][b]==0):
							slot2 = b
							slots[period-1][b] += 2
							alloc2 = 1
						else:
							control += 1
							if(control%2==1 and b-control!=a):
								b -= control
								if(b<0 and b+1+control!=a): control += 1; b += control
							elif(b+control!=a):
								b += control
								if(b>9): control += 1; b -= control
							else: pass
							if(waste==0 and not(0<=b<=9) and a!=5):
								b = 5
								control = 0
								waste = 1
							elif(waste==1 and not(0<=b<=9)):
								alloc2 = -1
								print('ALLOC ERROR 2 in alloc2, ',hpw,period,'\n',slots)
					while(alloc3==0):
						if(c_mod==0):
							if(a%2==0 and a+1<=9 and a+1!=b): c = a+1
							elif(a-1>=0 and a-1!=b): c = a-1
							else: pass
						elif(c_mod==1):
							if(a%2==0 and b+1<=9 and b+1!=a): c = b+1
							elif(b-1>=0 and b-1!=a): c = b-1
							else:pass
						elif(c_mod==2 and 0!=a and 0!=b):
							c = 0
						else: c_mod -= 1
						c_mod += 1
						if(slots[period-1][c]==1 and waste==0):
							slot3 = c
							slots[period-1][c] += 1
							alloc3 = 1
						elif(slots[period-1][c]==0 and waste==1):
							slot3 = c
							slots[period-1][c] += 1
							alloc3 = 1
						else:
							while(c+1==a or c+1==b):
								c += 1
						if(c==10 and (waste==0 and c_mod>2) and 0!=a and 0!=b):
							c = 0
							waste = 1
						elif(c==10 and (waste==1 and c_mod>2)):
							alloc3 = -1
						else: pass
					if(alloc==-1 or (alloc2==-1 or alloc3==-1)):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
						errors += 1
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor = getProf(sbj,candidates,period)
							gotProf = gotProf
							info = [sbj,period,hpw,professor,i,slot,slot2,slot3]
							if(profSche[professor][period-1][slot]==0 and (profSche[professor][period-1][slot2]==0 and profSche[professor][period-1][slot3]<2)):
								profSche[professor][period-1][slot] += 2
								profSche[professor][period-1][slot2] += 2
								profSche[professor][period-1][slot3] += 1
								sbjSche[sbj][period-1][slot] += 2
								sbjSche[sbj][period-1][slot2] += 2
								sbjSche[sbj][period-1][slot3] += 1
								gotProf = 1
							else: profPos += 1
							if(t>len(candidates)**2): gotProf = -1; print('Fatal error: No professors available at all!')
							elif(professor==-1): gotProf = -1; print('Unexisting professor got!')

				empty = 0
				try: sbjBook[sbj]
				except: empty = 1
				if(empty==1): sbjBook[sbj] = [info]
				else: x = sbjBook[sbj]; x.append(info)

				empty = 0
				try: profBook[professor]
				except: empty = 1
				if(empty==1): profBook[professor] = [info]
				else: y = profBook[professor]; y.append(info)
				
				if(0<=info[5]<=1):
					week_message1 = "Mondays"
				elif(2<=info[5]<=3):
					week_message1 = "Tuesdays"
				elif(4<=info[5]<=5):
					week_message1 = "Wednesdays"
				elif(6<=info[5]<=7):
					week_message1 = "Thursdays"
				else:
					week_message1 = "Fridays"
					
				if(info[5]%2==0 and info[1]==1):
					hour_message1 = "from 8:00 am to 10:00 am"
				elif(info[5]%2==0 and info[1]==2):
					hour_message1 = "from 2:00 pm to 4:00 pm"
				elif(info[5]%2==0 and info[1]==3):
					hour_message1 = "from 7:00 pm to 9:00 pm"
				elif(info[5]%2==1 and info[1]==1):
					hour_message1 = "from 10:00 am to 12:00 pm"
				elif(info[5]%2==1 and info[1]==2):
					hour_message1 = "from 4:00 pm to 6:00 pm"
				else:
					hour_message1 = "from 9:00 pm to 11:00 pm"
					
				if(len(info)>6):
					if(0<=info[6]<=1):
						week_message2 = "and Mondays"
					elif(2<=info[6]<=3):
						week_message2 = "and Tuesdays"
					elif(4<=info[6]<=5):
						week_message2 = "and Wednesdays"
					elif(6<=info[6]<=7):
						week_message2 = "and Thursdays"
					else:
						week_message2 = "and Fridays"
				
					if(info[6]%2==0 and info[1]==1):
						hour_message2 = "from 8:00 am to 10:00 am"
					elif(info[6]%2==0 and info[1]==2):
						hour_message2 = "from 2:00 pm to 4:00 pm"
					elif(info[6]%2==0 and info[1]==3):
						hour_message2 = "from 7:00 pm to 9:00 pm"
					elif(info[6]%2==1 and info[1]==1):
						hour_message2 = "from 10:00 am to 12:00 pm"
					elif(info[6]%2==1 and info[1]==2):
						hour_message2 = "from 4:00 pm to 6:00 pm"
					elif(info[6]%2==1 and info[1]==3):
						hour_message2 = "from 9:00 pm to 11:00 pm"
				else:
					week_message2 = '\b'
					hour_message2 = '\b'
				
				if(len(info)==8):
					if(0<=info[7]<=1):
						week_message3 = "and Mondays"
					elif(2<=info[7]<=3):
						week_message3 = "and Tuesdays"
					elif(4<=info[7]<=5):
						week_message3 = "and Wednesdays"
					elif(6<=info[7]<=7):
						week_message3 = "and Thursdays"
					else:
						week_message3 = "and Fridays"
				
					if(info[7]%2==0 and info[1]==1):
						hour_message3 = "from 8:00 am to 10:00 am"
					elif(info[7]%2==0 and info[1]==2):
						hour_message3 = "from 2:00 pm to 4:00 pm"
					elif(info[7]%2==0 and info[1]==3):
						hour_message3 = "from 7:00 pm to 9:00 pm"
					elif(info[7]%2==1 and info[1]==1):
						hour_message3 = "from 10:00 am to 12:00 pm"
					elif(info[7]%2==1 and info[1]==2):
						hour_message3 = "from 4:00 pm to 6:00 pm"
					elif(info[7]%2==1 and info[1]==3):
						hour_message3 = "from 9:00 pm to 11:00 pm"
				else:
					week_message3 = '\b'
					hour_message3 = '\b'

				print('Professor %i was assigned to teach the subject %i on' % (info[3],info[0]),week_message1,hour_message1,week_message2,hour_message2,week_message3,hour_message3,'\b.')
				
				if(sbj!=info[0]): print('ERROR 001')

				repeat -= 1
				if(repeat==0): period = 1
				
		for j in range(3):
			for k in range(10):
				if(slots[j][k]==0):
					sbj = -1
					professor = -1
					info = [sbj,j+1,2,professor,i,k]
					
					empty = 0
					try: sbjBook[sbj]
					except: empty = 1
					if(empty==1): sbjBook[sbj] = [info]
					else: x = sbjBook[sbj]; x.append(info)

					empty = 0
					try: profBook[professor]
					except: empty = 1
					if(empty==1): profBook[professor] = [info]
					else: y = profBook[professor]; y.append(info)
		
#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#

	#for i in range(len(sbjGroups)): # iterate for all subject groups
	for i in range(0): # iterate for all subject groups
		abort = 0
		for j in range(5): # each group is composed by 5 subjects
			slots2 = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
			sbj = sbjGroups[i][j] # obtain the current subject number
			candidates = list(candAval[j+5*i])
			candOrdered = sorted(candidates, key=lambda item: item[0], reverse=True)
			hpw = sbjHPW[sbj] # get the hours per week for this subject
			period = sbjPeriod[sbj]
			profPos = 0
			force = 0
			profSche_temp = list(profSche)
			sbjBook_temp = copy.deepcopy(sbjBook)
			profBook_temp = copy.deepcopy(profBook)
			
			# mod -> 0: just one period; 1: morning and night
			if(period==1): repeat = 1
			else: repeat = 0
			while(repeat>=0):
				alloc = 0
				if(repeat==1 and period==1): period = 3
				else: pass
				# Get the slots that will be occupied
				t = 0
				count = 0
				for k in range(10): #sbjSche[sbj][period-1]:
					#original = slots[period-1][k]
					original = sbjSche[sbj][period-1][k]
					if(original!=0):
						count += 1
						if(count==1):
							if(k%2==0):
								slot = k+1
								slots2[period-1][slot] = original
							else:
								slot = k-1
								slots2[period-1][slot] = original
						elif(count==2):
							if(k%2==0):
								slot2 = k+1
								slots2[period-1][slot2] = original
							else:
								slot2 = k-1
								slots2[period-1][slot2] = original
						else:
							if(k%2==0):
								slot3 = k+1
								slots2[period-1][slot3] = original
							else:
								slot3 = k-1
								slots2[period-1][slot3] = original
						if(count>3): print('ERROR!!!')
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor = getProf(sbj,candidates,period)
							gotProf = gotProf
							if(hpw==2 and count==1):
								info = [sbj,period,hpw,professor,i,slot]
							elif(2<hpw<5 and count==2):
								info = [sbj,period,hpw,professor,i,slot,slot2]
							elif(hpw==5 and count==3):
								info = [sbj,period,hpw,professor,i,slot,slot2,slot3]
							else: pass
							if(profSche[professor][period-1][slot]==0):
								profSche_temp[professor][period-1][slot] += 2
								gotProf = 1
							else: profPos += 1
							if(t>len(candidates)**2):
								gotProf = -1
								abort = 1
							else: pass
						
					else: pass
					
				empty = 0
				try: sbjBook_temp[sbj]
				except: empty = 1
				if(empty==1): sbjBook_temp[sbj] = [info]
				else: x = sbjBook_temp[sbj]; x.append(info)

				empty = 0
				try: profBook_temp[professor]
				except: empty = 1
				if(empty==1): profBook_temp[professor] = [info]
				else: y = profBook_temp[professor]; y.append(info)
				#print('SLOTS:\n',slots[period-1],'\nSLOTS2:\n',slots2[period-1])
				
				if(0<=info[5]<=1):
					week_message1 = "Mondays"
				elif(2<=info[5]<=3):
					week_message1 = "Tuesdays"
				elif(4<=info[5]<=5):
					week_message1 = "Wednesdays"
				elif(6<=info[5]<=7):
					week_message1 = "Thursdays"
				else:
					week_message1 = "Fridays"
					
				if(info[5]%2==0 and info[1]==1):
					hour_message1 = "from 8:00 am to 10:00 am"
				elif(info[5]%2==0 and info[1]==2):
					hour_message1 = "from 2:00 pm to 4:00 pm"
				elif(info[5]%2==0 and info[1]==3):
					hour_message1 = "from 7:00 pm to 9:00 pm"
				elif(info[5]%2==1 and info[1]==1):
					hour_message1 = "from 10:00 am to 12:00 pm"
				elif(info[5]%2==1 and info[1]==2):
					hour_message1 = "from 4:00 pm to 6:00 pm"
				else:
					hour_message1 = "from 9:00 pm to 11:00 pm"
					
				if(len(info)>6):
					if(0<=info[6]<=1):
						week_message2 = "and Mondays"
					elif(2<=info[6]<=3):
						week_message2 = "and Tuesdays"
					elif(4<=info[6]<=5):
						week_message2 = "and Wednesdays"
					elif(6<=info[6]<=7):
						week_message2 = "and Thursdays"
					else:
						week_message2 = "and Fridays"
				
					if(info[6]%2==0 and info[1]==1):
						hour_message2 = "from 8:00 am to 10:00 am"
					elif(info[6]%2==0 and info[1]==2):
						hour_message2 = "from 2:00 pm to 4:00 pm"
					elif(info[6]%2==0 and info[1]==3):
						hour_message2 = "from 7:00 pm to 9:00 pm"
					elif(info[6]%2==1 and info[1]==1):
						hour_message2 = "from 10:00 am to 12:00 pm"
					elif(info[6]%2==1 and info[1]==2):
						hour_message2 = "from 4:00 pm to 6:00 pm"
					elif(info[6]%2==1 and info[1]==3):
						hour_message2 = "from 9:00 pm to 11:00 pm"
				else:
					week_message2 = '\b'
					hour_message2 = '\b'
				
				if(len(info)==8):
					if(0<=info[7]<=1):
						week_message3 = "and Mondays"
					elif(2<=info[7]<=3):
						week_message3 = "and Tuesdays"
					elif(4<=info[7]<=5):
						week_message3 = "and Wednesdays"
					elif(6<=info[7]<=7):
						week_message3 = "and Thursdays"
					else:
						week_message3 = "and Fridays"
				
					if(info[7]%2==0 and info[1]==1):
						hour_message3 = "from 8:00 am to 10:00 am"
					elif(info[7]%2==0 and info[1]==2):
						hour_message3 = "from 2:00 pm to 4:00 pm"
					elif(info[7]%2==0 and info[1]==3):
						hour_message3 = "from 7:00 pm to 9:00 pm"
					elif(info[7]%2==1 and info[1]==1):
						hour_message3 = "from 10:00 am to 12:00 pm"
					elif(info[7]%2==1 and info[1]==2):
						hour_message3 = "from 4:00 pm to 6:00 pm"
					elif(info[7]%2==1 and info[1]==3):
						hour_message3 = "from 9:00 pm to 11:00 pm"
				else:
					week_message3 = '\b'
					hour_message3 = '\b'

				print('Professor %i was assigned to teach the subject %i on' % (info[3],info[0]),week_message1,hour_message1,week_message2,hour_message2,week_message3,hour_message3,'\b.')
				
				if(sbj!=info[0]): print('ERROR 002')
					
				repeat -= 1
				if(repeat==0): period = 1
				
		for j in range(3):
			for k in range(10):
				if(slots[j][k]==0):
					sbj = -1
					professor = -1
					info = [sbj,j+1,2,professor,i,k]
						
					empty = 0
					try: sbjBook_temp[sbj]
					except: empty = 1
					if(empty==1): sbjBook_temp[sbj] = [info]
					else: x = sbjBook_temp[sbj]; x.append(info)

					empty = 0
					try: profBook_temp[professor]
					except: empty = 1
					if(empty==1): profBook_temp[professor] = [info]
					else: y = profBook_temp[professor]; y.append(info)
				
		if(abort==0):
			profSche = list(profSche_temp)
			sbjBook = copy.deepcopy(sbjBook_temp)
			profBook = copy.deepcopy(profBook_temp)
		else: pass

#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#

	for i in range(p):
		prof_hpw = 0
		book = 1
		
		try: profBook[i]
		except: book = 0
		
		if(book==1):
			for j in profBook[i]:
				prof_hpw += j[2]
		else: pass
		
		attempt = 0
		invert = 0
		while(prof_hpw<20):
			try: sbj = profSubject[i][attempt]
			except:
				attempt = 0
				invert = 2
				sbj = profSubject[i][0]
			hpw = sbjHPW[sbj]
			period = sbjPeriod[sbj]
			try: group = sbjBook[sbj][0][4]
			except: group = None
			
			if(period==1 and (profPeriod[i][0]==2 or profPeriod[i][2]==1)): period = 1+invert
			else: period = 3-invert
			pref_slots0 = []
			pref_slots1 = []
			a = None
			b = None
			c = None
			
			schedule = profSche[i][period-1]
			
			for j in range(10):
				mod = j%2
				if(schedule[j]>0 and schedule[j-2*mod+1]==0): pref_slots0.append(j-2*mod+1)
				else: pass
					
			for j in range(10):
				if(schedule[j]==1): pref_slots1.append(j)
				else: pass
					
			try: a = pref_slots0[0]
			except:
				for j in range(10):
					if(schedule[j]==0):
						a = j
						break
					else: pass
			
			if(hpw==2 and a!=None):
				info = [sbj,period,hpw,i,group,a]
				profSche[i][period-1][a] += 2
				sbjSche[sbj][period-1][a] += 2
				prof_hpw += 2
				valid = 1
				
			elif(hpw==3 and a!=None):
				try: b = pref_slots1[0]
				except: 
					if(a%2==0): mod = 1
					else: mod = -1
					for j in range(4,-1,-1):
						if(9>=a+j+mod>=0 and schedule[a+j+mod]<2 and ((a+j+mod in pref_slots0) or (a+j+mod in pref_slots1))):
							b = a+j+mod
							break
					else:
						for j in range(4,-1,-1):
							if(9>=a+j+mod>=0 and schedule[a+j+mod]<2):
								b = a+j+mod
								break
				
				if(b!=None):	
					info = [sbj,period,hpw,i,group,a,b]
					profSche[i][period-1][a] += 2
					sbjSche[sbj][period-1][a] += 2
					profSche[i][period-1][b] += 1
					sbjSche[sbj][period-1][b] += 1
					prof_hpw += 3
					valid = 1
				else: valid = 0
				
			elif(hpw==4 and a!=None):
				if(a%2==0): mod = 1
				else: mod = -1
				for j in range(4,-1,-1):
					if(9>=a+j+mod>=0 and schedule[a+j+mod]==0 and ((a+j+mod in pref_slots0) or (a+j+mod in pref_slots1))):
						b = a+j+mod
						break
				else:
					for j in range(4,-1,-1):
						if(9>=a+j+mod>=0 and schedule[a+j+mod]==0):
							b = a+j+mod
							break
				if(b!=None):
					info = [sbj,period,hpw,i,group,a,b]
					profSche[i][period-1][a] += 2
					sbjSche[sbj][period-1][a] += 2
					profSche[i][period-1][b] += 2
					sbjSche[sbj][period-1][b] += 2
					prof_hpw += 4
					valid = 1
				else: valid = 0
				
			elif(hpw==5 and a!=None):
				if(a%2==0): mod = 1
				else: mod = -1
				
				for j in range(4,-1,-1):
					if(9>=a+j+mod>=0 and schedule[a+j+mod]==0 and ((a+j+mod in pref_slots0) or (a+j+mod in pref_slots1))):
						b = a+j+mod
						break
				else:
					for j in range(4,-1,-1):
						if(9>=a+j+mod>=0 and schedule[a+j+mod]==0):
							b = a+j+mod
							break
				
				if(b%2==0): mod2 = 1
				else: mod2 = -1
				
				if(schedule[a+mod]<2): c = a+mod
				elif(schedule[b+mod2]<2): c = b+mod2
				else:
					for j in range(10):
						if(schedule[j]<2):
							c = j
							break
						else: pass
				if(b!=None and c!=None):
					info = [sbj,period,hpw,i,group,a,b,c]
					profSche[i][period-1][a] += 2
					sbjSche[sbj][period-1][a] += 2
					profSche[i][period-1][b] += 2
					sbjSche[sbj][period-1][b] += 2
					profSche[i][period-1][c] += 1
					sbjSche[sbj][period-1][c] += 1
					prof_hpw += 5
					valid = 1
				else: valid = 0
			else: valid = 0
			
			if(valid==1):
				empty = 0
				try: sbjBook[sbj]
				except: empty = 1
				if(empty==1): sbjBook[sbj] = [info]
				else: x = sbjBook[sbj]; x.append(info)

				empty = 0
				try: profBook[i]
				except: empty = 1
				if(empty==1): profBook[i] = [info]
				else: y = profBook[i]; y.append(info)
			
				if(0<=info[5]<=1):
					week_message1 = "Mondays"
				elif(2<=info[5]<=3):
					week_message1 = "Tuesdays"
				elif(4<=info[5]<=5):
					week_message1 = "Wednesdays"
				elif(6<=info[5]<=7):
					week_message1 = "Thursdays"
				else:
					week_message1 = "Fridays"
				
				if(info[5]%2==0 and info[1]==1):
					hour_message1 = "from 8:00 am to 10:00 am"
				elif(info[5]%2==0 and info[1]==2):
					hour_message1 = "from 2:00 pm to 4:00 pm"
				elif(info[5]%2==0 and info[1]==3):
					hour_message1 = "from 7:00 pm to 9:00 pm"
				elif(info[5]%2==1 and info[1]==1):
					hour_message1 = "from 10:00 am to 12:00 pm"
				elif(info[5]%2==1 and info[1]==2):
					hour_message1 = "from 4:00 pm to 6:00 pm"
				else:
					hour_message1 = "from 9:00 pm to 11:00 pm"
				
				if(len(info)>6):
					if(0<=info[6]<=1):
						week_message2 = "and Mondays"
					elif(2<=info[6]<=3):
						week_message2 = "and Tuesdays"
					elif(4<=info[6]<=5):
						week_message2 = "and Wednesdays"
					elif(6<=info[6]<=7):
						week_message2 = "and Thursdays"
					else:
						week_message2 = "and Fridays"
			
					if(info[6]%2==0 and info[1]==1):
						hour_message2 = "from 8:00 am to 10:00 am"
					elif(info[6]%2==0 and info[1]==2):
						hour_message2 = "from 2:00 pm to 4:00 pm"
					elif(info[6]%2==0 and info[1]==3):
						hour_message2 = "from 7:00 pm to 9:00 pm"
					elif(info[6]%2==1 and info[1]==1):
						hour_message2 = "from 10:00 am to 12:00 pm"
					elif(info[6]%2==1 and info[1]==2):
						hour_message2 = "from 4:00 pm to 6:00 pm"
					elif(info[6]%2==1 and info[1]==3):
						hour_message2 = "from 9:00 pm to 11:00 pm"
				else:
					week_message2 = '\b'
					hour_message2 = '\b'
			
				if(len(info)==8):
					if(0<=info[7]<=1):
						week_message3 = "and Mondays"
					elif(2<=info[7]<=3):
						week_message3 = "and Tuesdays"
					elif(4<=info[7]<=5):
						week_message3 = "and Wednesdays"
					elif(6<=info[7]<=7):
						week_message3 = "and Thursdays"
					else:
						week_message3 = "and Fridays"
			
					if(info[7]%2==0 and info[1]==1):
						hour_message3 = "from 8:00 am to 10:00 am"
					elif(info[7]%2==0 and info[1]==2):
						hour_message3 = "from 2:00 pm to 4:00 pm"
					elif(info[7]%2==0 and info[1]==3):
						hour_message3 = "from 7:00 pm to 9:00 pm"
					elif(info[7]%2==1 and info[1]==1):
						hour_message3 = "from 10:00 am to 12:00 pm"
					elif(info[7]%2==1 and info[1]==2):
						hour_message3 = "from 4:00 pm to 6:00 pm"
					elif(info[7]%2==1 and info[1]==3):
						hour_message3 = "from 9:00 pm to 11:00 pm"
				else:
					week_message3 = '\b'
					hour_message3 = '\b'

				print('Professor %i was assigned to teach the subject %i on' % (info[3],info[0]),week_message1,hour_message1,week_message2,hour_message2,week_message3,hour_message3,'\b.')
			
				if(sbj!=info[0]): print('ERROR 003')

				attempt += 1
			else:
				attempt += 1

	####	####	####	####	####	####	####	####	####	####
	####	####	####	####	####	####	####	####	####	####
	a_test = 0								####
	b_test = 0								####
	for p_test in range(p):				                        ####
		for i_test in range(len(profBook[p_test])):			####
			for j_test in range(5,len(profBook[p_test][i_test])):	####
				a_test += 2					####
			if(profBook[p_test][i_test][2]%2==1): a_test -= 1	####
		for j_test in range(len(profSche[p_test])):			####
			b_test += sum(profSche[p_test][j_test])			####
		if(b_test==a_test): pass					####
		else: print("Schedule Error!\n"+str(profBook[p_test])+"\n"+str(profSche[p_test])); y_fool = z_null				####
	####	####	####	####	####	####	####	####	####	####
	####	####	####	####	####	####	####	####	####	####
	print("passed 1039")
	return

###########################################################################################
def initSolution(p):
	# Declare global variables
	global candAval
	global profSche
	# Create empty lists and dictionaries
	candAval = []
	profSche = []
	for i in range(p):
		profSche.append([[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]])

	# Obtain an avaliation of the possibility of each professor for teaching a certain subject
	for i in range(len(sbjGroups)): # make the avalitaion for subjects into subject groups
		for j in range(5): # each group has 5 subjects
			sbj = sbjGroups[i][j] # get current subject number
			candidates = sbjProfs[i] # get the list of candidates for teaching this subject
			groupAval = []
			for k in range(len(candidates)):
				aval = 0 # starting score is 0, maximum score is 5
				if(sbjPeriod[sbj]==1 and (profPeriod[candidates[k][0]][0]==2 and profPeriod[candidates[k][0]][2]!=2)): aval += 1 # 1 point if period is partially matching
				elif(sbjPeriod[sbj]==1 and (profPeriod[candidates[k][0]][2]==2 and profPeriod[candidates[k][0]][0]!=2)): aval += 1
				elif(sbjPeriod[sbj]==1 and (profPeriod[candidates[k][0]][0]==2 and profPeriod[candidates[k][0]][2]==2)): aval += 2 # 2 points for exact period matching
				elif(sbjPeriod[sbj]==2 and profPeriod[candidates[k][0]][1]==2): aval += 2
				elif(profPeriod[candidates[k][0]][0]==profPeriod[candidates[k][0]][1]==profPeriod[candidates[k][0]][2]): aval += 1
				else: pass
				aval += 3-candidates[k][1]
				groupAval.append([aval,candidates[k][0]]) # store avaliation of this professor in this subject group
			candAval.append(groupAval) # store the avaliation of all professors in all subject groups

	assign(p)

	return

###########################################################################################
def help():
	f = open('variables', 'w')
	str1 = ', '.join(str(e) for e in sbjGroups)
	str2 = ', '.join(str(e) for e in profSubject)
	str3 = ', '.join(str(e) for e in sbjProfs)
	str4 = ', '.join(str(e) for e in candAval)
	str5 = ', '.join(str(e) for e in profPeriod)
	str6 = ', '.join(str(e) for e in sbjPeriod)
	str7 = ', '.join(str(e) for e in sbjHPW)
	str8 = ', '.join(str(e) for e in sbjOrdered)
	str9 = ', '.join('{}{}'.format(key, val) for key, val in sorted(sbjBook.items()))
	str10 = ', '.join('{}{}'.format(key, val) for key, val in sorted(profBook.items()))
	str11 = ', '.join(str(e) for e in profSche)
	str12 = ', '.join(str(e) for e in sbjSche)
	string = 'sbjGroups:\n'+str1+'   '+str(len(sbjGroups))+'\n\n'+'profSubject:\n'+str2+'   '+str(len(profSubject))+'\n\n'+'sbjProfs:\n'+str3+'   '+str(len(sbjProfs))+'\n\n'+'candAval:\n'+str4+'   '+str(len(candAval))+'\n\n'+'profPeriod:\n'+str5+'   '+str(len(profPeriod))+'\n\n'+'sbjPeriod:\n'+str6+'   '+str(len(sbjPeriod))+'\n\n'+'sbjHPW:\n'+str7+'   '+str(len(sbjHPW))+'\n\n'+'sbjOrdered:\n'+str8+'   '+str(len(sbjOrdered))+'\n\n'+'sbjBook:\n'+str9+'   '+str(len(sbjBook))+'\n\n'+'profBook:\n'+str10+'   '+str(len(profBook))+'\n\n'+'profSche:\n'+str11+'   '+str(len(profSche))+'\n\n'+'sbjSche:\n'+str12+'   '+str(len(sbjSche))+'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
	f.write(string)
	
	return


###########################################################################################
def getNeighborhood():
	neighborhood = []
	
	# Compactness movements, i.e. subject & professor exchanges
	
	for i in range(len(sbjGroups)): # Make one permutation for each subject group
		for j in range(5): # Each group has 5 subjects
			sbj = sbjGroups[i][j] # Get the current subject number
			hpw = sbjHPW[sbj] # Get hours per week
			s = int(hpw/2)+hpw%2 # Get number of slots that this subject requires
			while(s!=0): # Make the permutation for one slot at a time
				for k in range(len(sbjBook[sbj])): # Pick one period and professor that will be offering this subject
					professor = sbjBook[sbj][k][3] # Get the professor number
					info = sbjBook[sbj][k] # Get the subject info (info = [subject,period,hpw,professor,group,slot,slot2,slot3])
					period = info[1]
					from_slot = info[4+s] # Get the slot from which the subject will be moved
					destinations = list(range(10)) # Get a list of possible slot destinations
					destinations.remove(from_slot) # Remove from the list the slot that the subject is being moved from
					for slot in destinations: # Try to create a neighbor for each possible destination
						for l in range(5): # The destination can be being occupied by any of the groups' subject, even the same subject which is being moved
							sbj2 = sbjGroups[i][l] # Get the number of the subject that is occupying the destination slot
							hpw2 = sbjHPW[sbj2] # Get hours per week
							for m in range(len(sbjBook[sbj2])): # Pick one period and professor that will be offering this subject
								sbj2_info = sbjBook[sbj2][m] # Get subject 2 info
								period2 = sbj2_info[1]
								professor2 = sbj2_info[3] # Get professor 2
								for n in range(int(sbj2_info[2]/2)+sbj2_info[2]%2): # Iterate for all the slots that this subject occupies
									if(i==info[4]==sbj2_info[4] and (slot==sbj2_info[5+n] and period==period2)): # Check if one of the slots that are occupied by this subject is the destination slot
										num_slots = int(hpw/2)+hpw%2
										num_slots2 = int(hpw2/2)+hpw2%2
										if(professor==professor2 and professor!=-1):
											permute = 1
										elif(professor==professor2 and professor==-1):
											permute = 0
										elif(professor2==-1 and professor!=-1):
											permute = 1
										#elif(((hpw==3 and s==1) or (hpw==5 and s==2)) and ((hpw2==3 and n==1) or (hpw2==5 and n==2))):
										#	for o in range(len(profBook[professor2])):
										#		if(profBook[professor2][o][1]==period and profBook[professor2][o][0]==sbj2):
										#			if(profBook[professor2][o][5+n]==from_slot or (profBook[professor2][o][2]))
										elif((hpw2==3 and n==1) or (hpw2==5 and n==2)):
											for o in range(len(profBook[professor2])):
												if(profBook[professor2][o][1]==period and profBook[professor2][o][0]==sbj2):
													if(profBook[professor2][o][5+n]==from_slot and (n!=2 or ((hpw!=3 and s!=2) and (hpw!=5 and s!=3)))):
														permute = 0
														break
													else:
														try: permute
														except:
															permute = 1
												else: pass
										else:
											for o in range(len(profBook[professor2])):
												if(profBook[professor2][o][1]==period and profBook[professor2][o][0]==sbj2):
													if(profBook[professor2][o][5+n]==from_slot):
														permute = 0
														break
													else:
														try: permute
														except:
															permute = 1
										if((hpw==3 and num_slots==2) or (hpw==5 and num_slots==3)):
											for o in range(len(profBook[professor])):
												if(profBook[professor][o][1]==period and profBook[professor][o][0]==sbj2):
													if(profBook[professor][o][5+n]==from_slot and (n!=2 or ((hpw!=3 and s!=2) and (hpw!=5 and s!=3)))):
														permute = 0
														break
													else:
														try: permute
														except:
															permute = 1
												else: pass
										else:
											for o in range(len(profBook[professor])):
												if(profBook[professor][o][1]==period and profBook[professor][o][0]==sbj2):
													if(profBook[professor][o][5+n]==from_slot):
														permute = 0
														break
													else:
														try: permute
														except:
															permute = 1
										for o in range(len(info)-5):
											if(info[5+o]==sbj2_info[5+n]):
												permute = 0
											else: pass
											
										for o in range(len(sbj2_info)-5):
											if(sbj2_info[5+o]==info[4+s]):
												permute = 0
											else: pass
										
										if(permute==1):
											new_info1 = copy.deepcopy(info)
											new_info1[4+s] = sbj2_info[5+n]
											new_info2 = copy.deepcopy(sbj2_info)
											new_info2[5+n] = info[4+s]
											cost = getCost(info,sbj2_info,new_info1,new_info2)
											neighbor = (info,sbj2_info,new_info1,new_info2,cost)
											if(neighbor in neighborhood): pass
											else: neighborhood.append(neighbor)
											if(info[4]!=sbj2_info[4]): print("Error! Permutation being made between different subject groups!",i,info[4],sbj2_info[4])
											elif(info[1]!=sbj2_info[1]): print("Error! Permutation being made between different periods!")
											#print(info,sbj2_info,'\n',new_info1,new_info2,'\n')
										else: pass
									else: pass
	
				s -= 1
				
	for i in sbjBook: # Make permutations for subjects that are outside subject groups
		for j in range(len(sbjBook[i])):
			info = sbjBook[i][j]
			professor = info[3]
			sbj = info[0]
			period = info[1]
			hpw = info[2]
			for k in range(len(info)-5):
				from_slot = info[5+k]
				if(info[4]==None and info[0]!=-1): # This subject isn't in any subject group and it is actually being offered
					for l in range(10): # iterate for all the slots
						if((profSche[professor][period-1][l]==0 or (profSche[professor][period-1][l]==1 and (hpw%2==1 and k+6==len(info)))) and from_slot!=l):
							#print(l,profSche[professor][period-1],profSche[professor][period-1][l])
							new_info = copy.deepcopy(info)
							new_info[5+k] = l
							ghost_info = [-1,period,2,-1,None,l]
							new_ghost_info = [-1,period,2,-1,None,from_slot]
							cost = getCost(info,ghost_info,new_info,new_ghost_info)
							neighbor = (info,ghost_info,new_info,new_ghost_info,cost)
							if(neighbor in neighborhood): pass
							else: neighborhood.append(neighbor)
							#print('\nHEY\n',info,ghost_info,'\n',new_info,ghost_info,'\n')
						else: pass

	# Subject and period preferences movements, i.e. professor exchanges
	for i in sbjBook:
		for j in range(len(sbjBook[i])):
			info = sbjBook[i][j]
			professor = info[3]
			sbj = info[0]
			period = info[1]
			hpw = info[2]
			group = info[4]
			schedule = profSche[professor]
			sbj_slots = []
			for k in range(len(info)-5):
				sbj_slots.append(info[5+k])
			for k in sbjBook:
				for l in range(len(sbjBook[k])):
					info2 = sbjBook[k][l]
					professor2 = info2[3]
					sbj2 = info2[0]
					period2 = info2[1]
					hpw2 = info2[2]
					group2 = info2[4]
					schedule2 = profSche[professor2]
					sbj2_slots = []
					for m in range(len(info2)-5):
						sbj2_slots.append(info2[5+m])
					# professor exchange
					if(professor==professor2 or professor==-1 or professor2==-1): pass
					else:
						if(sbj in profSubject[professor2] and sbj2 in profSubject[professor]):
							count = 0
							for m in sbj2_slots:
								count += 1
								if(schedule[period2-1][m]==0 or (m in sbj_slots and period==period2 and (not(count==len(info2)-5 and hpw2%2==1) or ((count==len(info2)-5 and hpw2%2==1) and ( hpw%2==1 and info[-1]==m )))) or (schedule[period2-1][m]==1 and count==len(info2)-5 and hpw2%2==1)):
									try: permute
									except: permute = 1
								else: permute = 0
							count = 0
							for n in sbj_slots:
								count += 1
								if(schedule2[period-1][n]==0 or (n in sbj2_slots and period==period2 and (not(count==len(info)-5 and hpw%2==1) or ((count==len(info)-5 and hpw%2==1) and ( hpw2%2==1 and info2[-1]==n )))) or (schedule2[period-1][n]==1 and count==len(info)-5 and hpw%2==1)):
									try: permute
									except: permute = 1
								else: permute = 0
							if(sbj==sbj2 and period==period2): permute = 0
							else: pass
							if(permute==1):
								new_info2 = copy.deepcopy(info)
								new_info2[3] = professor2
								new_info = copy.deepcopy(info2)
								new_info[3] = professor
								cost = getCost(info,info2,new_info,new_info2)
								neighbor = (info,info2,new_info,new_info2,cost)
								if(neighbor in neighborhood): pass
								else: neighborhood.append(neighbor)#; print('HAHA',neighbor)
							else: pass

	return neighborhood

###########################################################################################
def getCost(orig1,orig2,move1,move2):
	cost = 0
	if(orig1[3]!=orig2[3]):
		for i,j in (move1,orig1),(move2,orig2):
			if(i[3]==-1): pass
			else:
				sbj = i[0]
				osbj = j[0]
				prof = i[3]
				period = i[1]-1
				operiod = j[1]-1
				sche = copy.deepcopy(profSche[prof])
				try:
					for k in range(3):
						sche[operiod][j[5+k]] = 0
				except: pass
				try:
					for k in range(3):
						sche[period][i[5+k]] = 2
					if(k==2): sche[period][i[5+k]] = 1
					else: pass
				except:
					if(i[2]%2==1): sche[period][i[4+k]] = 1
					else: pass
				osche = profSche[prof]
				# Subject preference satisfaction
					# Movement
				if(profSubject[prof][0]==sbj): pass
				elif(profSubject[prof][1]==sbj): cost += 1
				elif(profSubject[prof][2]==sbj): cost += 2
				else: cost += 3
					# Original
				if(profSubject[prof][0]==osbj): pass
				elif(profSubject[prof][1]==osbj): cost -= 1
				elif(profSubject[prof][2]==osbj): cost -= 2
				else: cost -= 3
				# Period preference satisfaction
					# Movement
				if(profPeriod[prof][period-1]==2): pass
				else: cost += 3
					# Original
				if(profPeriod[prof][operiod-1]==2): pass
				else: cost -= 3
				# Compactness of the schedule
					# Movement
				day = []
				for k in range(5):
					day.append([])
					for l in range(3):
						day[k].append(sche[l][0+2*k])
						day[k].append(sche[l][1+2*k])
						if(sche[l][0+2*k]!=0 or sche[l][1+2*k]!=0): cost += 1
						else: pass
				for k in range(5):
					for l in range(6):
						try:
							if(day[k][l]!=0 and (day[k][l-1]!=0 or day[k][l+1]!=0)): cost += 1
							elif(day[k][l]==0 and day[k][l-1]!=0 and day[k][l+1]!=0): cost += 2
							elif(day[k][l]!=0 and day[k][l-1]==0 and day[k][l+1]==0): cost += 3
							else: pass
						except:
							try:
								if(day[k][l]!=0 and day[k][l+1]==0): cost += 3
								elif(day[k][l]==0): pass
								else: cost += 1
							except:
								if(day[k][l]!=0 and day[k][l-1]==0): cost += 3
								elif(day[k][l]==0): pass
								else: cost += 1
					# Original
				day = []
				for k in range(5):
					day.append([])
					for l in range(3):
						day[k].append(osche[l][0+2*k])
						day[k].append(osche[l][1+2*k])
						if(osche[l][0+2*k]!=0 or osche[l][1+2*k]!=0): cost -= 1
						else: pass
				for k in range(5):
					for l in range(6):
						try:
							if(day[k][l]!=0 and (day[k][l-1]!=0 or day[k][l+1]!=0)): cost -= 1
							elif(day[k][l]==0 and day[k][l-1]!=0 and day[k][l+1]!=0): cost -= 2
							elif(day[k][l]!=0 and day[k][l-1]==0 and day[k][l+1]==0): cost -= 3
							else: pass
						except:
							try:
								if(day[k][l]!=0 and day[k][l+1]==0): cost -= 3
								elif(day[k][l]==0): pass
								else: cost -= 1
							except:
								if(day[k][l]!=0 and day[k][l-1]==0): cost -= 3
								elif(day[k][l]==0): pass
								else: cost -= 1	

	else: pass
	#print(cost)
	return cost
	
###########################################################################################
def getBest(BestIter,rejected):
	global global_lowest
	
	N = getNeighborhood()
	index = [None,None]
	addforward = 0
	bypass = 0
	lowest = 10**10
	try: global_lowest
	except: global_lowest = lowest
	
	for i in range(len(N)):
		if(N[i][-1] < lowest and N[i] not in rejected):
			BestMove = N[i]
			lowest = N[i][-1]
			if(lowest < global_lowest):
				global_lowest = lowest
				addforward = 1
			else: pass
		else: pass
	for i in range(2):
		for j in range(8):
			if(BestMove[0+i][j]!=BestMove[2+i][j]):
				index[i] = j
				break
			else: pass
	if(len(T)>7):
		del T[0]
		del Ti[0]
	else: pass
	for i in (2,3):
		if(BestMove[i] in T):
			pos = [y for y,x in enumerate(T) if x == BestMove[i]]
			pos = pos[0]
			if(index[i-2]==Ti[pos] and not lowest < global_lowest): bypass = 0
			else: bypass += 1
		else: bypass += 1
	
	if(bypass > 0):
		T.append(BestMove[2])
		T.append(BestMove[3])
		Ti.append(index[0])
		Ti.append(index[1])
		BestIter += addforward
	else:
		rejected.append(BestMove)
		BestMove, BestIter = getBest(BestIter,rejected)

	return BestMove, BestIter

###########################################################################################
def tabuSearch(Itermax):
	global T
	global Ti
	
	Iter = 0 
	BestIter = 0
	T = []
	Ti = []
	
	while(Iter-BestIter<Itermax):
		Iter += 1
		BestMove,BestIter = getBest(BestIter,[])

		# Update current solution with the movement picked
		pS1 = profSche[BestMove[0][3]]
		pS2 = profSche[BestMove[1][3]]
		sS1 = sbjSche[BestMove[2][0]]
		sS2 = sbjSche[BestMove[3][0]]
		sbj1 = BestMove[2][0]
		osbj1 = BestMove[0][0]
		sbj2 = BestMove[3][0]
		osbj2 = BestMove[1][0]
		hpw1 = BestMove[2][2]
		hpw2 = BestMove[3][2]
		ohpw1 = BestMove[0][2]
		ohpw2 = BestMove[1][2]
		prof1 = BestMove[0][3]
		prof2 = BestMove[1][3]
		period1 = BestMove[2][1]-1
		operiod1 = BestMove[0][1]-1
		period2 = BestMove[3][1]-1
		operiod2 = BestMove[1][1]-1
			# Update profSche
		if(prof1==-1): pass
		else:
			try:                                                            # 
				for k in range(3):                                      # 
					last = 0                                        # 
					try: pS1[operiod1][BestMove[0][6+k]]            #   ____________________
					except: last = 1                                #  | Clean old schedule |
					if(ohpw1%2==1 and last==1):                     #  |  from professor 1  |
						pS1[operiod1][BestMove[0][5+k]] -= 1    #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
					else:                         		        # 
						pS1[operiod1][BestMove[0][5+k]] -= 2  	# 
			except: pass                                         		# 
		if(prof2==-1): pass
		else:
			try:                                                            # 
				for k in range(3):                                      # 
					last = 0                                        # 
					try: pS2[operiod2][BestMove[1][6+k]]            #   ____________________
					except: last = 1                                #  | Clean old schedule |
					if(ohpw2%2==1 and last==1):                     #  |  from professor 2  |
						pS2[operiod2][BestMove[1][5+k]] -= 1    #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
					else:                         		        # 
						pS2[operiod2][BestMove[1][5+k]] -= 2  	# 
			except: pass                                         		# 
		if(prof1==-1): pass
		else:
			try:                                                                           #   
				for k in range(3):                                                     #
					last = 0                                                       #   ____________________
					try: pS1[period1][BestMove[2][6+k]]                            #  | Write new schedule |
					except: last = 1                                               #  |  for professor 1   |
					if(last==1 and hpw1%2==1): pS1[period1][BestMove[2][5+k]] += 1 #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
					else: pS1[period1][BestMove[2][5+k]] += 2                      # 
			except: pass                                                   		       #
		if(prof2==-1): pass
		else:
			try:                                                                           #   
				for k in range(3):                                                     #
					last = 0                                                       #   ____________________
					try: pS2[period2][BestMove[3][6+k]]                            #  | Write new schedule |
					except: last = 1                                               #  |  for professor 2   |
					if(last==1 and hpw2%2==1): pS2[period2][BestMove[2][5+k]] += 1 #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
					else: pS2[period2][BestMove[3][5+k]] += 2                      # 
			except: pass                                                   		       #
		
			# Update sbjSche
		if(osbj1==-1): pass
		else:
			try:                                                          # 
				for k in range(3):                                    # 
					last = 0                                      # 
					try: sS1[operiod1][BestMove[0][6+k]]          #   ____________________
					except: last = 1                              #  | Clean old schedule |
					if(ohpw1%2==1 and last==1):                   #  |   from subject 1   |
						sS1[operiod1][BestMove[0][5+k]] -= 1  #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
					else:                    		      #
						sS1[operiod1][BestMove[0][5+k]] -= 2  #
			except: pass                                                  # 
		if(osbj2==-1): pass
		else:
			try:                                                          # 
				for k in range(3):                                    # 
					last = 0                                      # 
					try: sS2[operiod2][BestMove[1][6+k]]          #   ____________________
					except: last = 1                              #  | Clean old schedule |
					if(ohpw2%2==1 and last==1):                   #  |   from subject 2   |
						sS2[operiod2][BestMove[1][5+k]] -= 1  #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
					else:                    		      #
						sS2[operiod2][BestMove[1][5+k]] -= 2  #
			except: pass                                                  # 
		if(sbj1==-1): pass
		else:
			try:                                                                             #   
				for k in range(3):                                                       #
					last = 0                                                         #   ____________________
					try: sS1[period1][BestMove[2][6+k]]                              #  | Write new schedule |
					except: last = 1                                                 #  |   for subject 1    |
					if(hpw1%2==1 and last==1): sS1[period1][BestMove[2][5+k]] += 1   #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯  
					else: sS1[period1][BestMove[2][5+k]] += 2                        #
			except: pass                                                                     #
		if(sbj2==-1): pass
		else:	
			try:                                                                             #   
				for k in range(3):                                                       #
					last = 0                                                         #   ____________________
					try: sS2[period2][BestMove[3][6+k]]                              #  | Write new schedule |
					except: last = 1                                                 #  |   for subject 2    |
					if(hpw2%2==1 and last==1): sS2[period2][BestMove[3][5+k]] += 1   #   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯  
					else: sS2[period2][BestMove[3][5+k]] += 2                        #
			except: pass                                                                     #
		
			# Update profBook
		profBook[prof1].remove(BestMove[0])
		profBook[prof1].append(BestMove[2])
		if(prof2!=-1):
			profBook[prof2].remove(BestMove[1])
			profBook[prof2].append(BestMove[3])
		else: pass
		
			# Update sbjBook
		sbjBook[osbj1].remove(BestMove[0])
		sbjBook[sbj1].append(BestMove[2])
		if(osbj2!=-1):
			sbjBook[osbj2].remove(BestMove[1])
			sbjBook[sbj2].append(BestMove[3])
		else: pass

	return

###########################################################################################
def main(p=50,Itermax=100):
	t0 = time.perf_counter()
	t0 = t0.as_integer_ratio()
	scenario(p)
	t1 = time.perf_counter()
	t1 = t1.as_integer_ratio()
	initSolution(p)
	t2 = time.perf_counter()
	t2 = t2.as_integer_ratio()
	tabuSearch(Itermax)
	t3 = time.perf_counter()
	t3 = t3.as_integer_ratio()
	help()
	print(getReport(p))
	print("\nScenario generated in",t1[0]/t1[1]-t0[0]/t0[1],"seconds","\nInitial solution generated in",t2[0]/t2[1]-t1[0]/t1[1],"seconds","\nTabu search run time:",t3[0]/t3[1]-t2[0]/t2[1],"seconds")

	return
	
errors = 0
run = 0
#for i in range(100):
profNumber = input("How many professors there will be in the university? ")
profNumber = int(profNumber)
iterNumber = input("How many iterations do you want Tabu Search algorithm to perform? ")
iterNumber = int(iterNumber)
main(profNumber, iterNumber)
#	run += 1
#	print('Run: ',run, end='\r')
#print('\n',errors,' errors')
#print("Subject Groups:\n")
#print(sbjGroups)
#print("\n\n")
#print("Professors Subjects:\n")
#print(profSubject)
#print("\n\n")
#print("Subjects Professors:\n")
#print(sbjProfs)
#print("\n\n")
#print("Cadidates Avalation:\n")
#print(candAval)
#print(sbjBook)

###########################################################################################
def printvars():

   tmp = globals().copy()
   [print(k,'  :  ',v,'\n') for k,v in tmp.items() if not k.startswith('_') and k!='tmp' and k!='In' and k!='Out' and not hasattr(v, '__call__')]

#printvars()














































