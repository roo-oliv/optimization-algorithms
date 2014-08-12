###########################################################################################	
###########################################################################################	
###########################################################################################	
def Professor(sbj,candidates,period,profPos,candOrdered,profPeriod):
	got = 0
	force = 0
	while(got==0):
		if(len(candOrdered)==profPos): profPos = 0; force = 1
		else: pass
		if(profPeriod[candOrdered[profPos][1]][period-1]==2 or force==1):
			period += 1
			professor = candOrdered[profPos][1]
			got = 1
		else:
			profPos += 1

	return professor, profPos

###########################################################################################	
###########################################################################################	
###########################################################################################	
def Neighborhood(sbjHPW, sbjGroups, sbjBook, profBook, sbjSche, profSche, profSubject, profPeriod):

	#from math import *
	import copy

	neighborhood = []
	for i in range(len(sbjGroups)): # Make one permutation for each subject group
		for j in range(5): # Each group has 5 subjects
			sbj1 = sbjGroups[i][j] # Get the current subject number
			hpw1 = sbjHPW[sbj1] # Get hours per week
			s1 = int(hpw1/2)+hpw1%2 # Get number of slots that this subject requires
			for k in range(s1):
				for l in range(len(sbjBook[sbj1])):
					prof1 = sbjBook[sbj1][l][3] # Get the professor number
					info1 = sbjBook[sbj1][l] # Get the subject info (info = [subject,period,hpw,professor,group,slot,slot2,slot3])
					period1 = info1[1]-1
					current1 = info1[5+k]
					if(k+1!=s1 or hpw1%2==0): cs1 = 2
					else: cs1 = 1
					for m in range(6): # The destination can be being occupied by any of the groups' subject, even the same subject which is being moved or not being occupied
						if(m==5):
							sbj2 = -1
							hpw2 = 2
							s2 = 1
						else:
							sbj2 = sbjGroups[i][m]
							hpw2 = sbjHPW[sbj2]
							s2 = int(hpw2/2)+hpw2%2
						for n in range(len(sbjBook[sbj2])):
							prof2 = sbjBook[sbj2][n][3] # Get the professor number
							info2 = sbjBook[sbj2][n] # Get the subject info (info = [subject,period,hpw,professor,group,slot,slot2,slot3])
							period2 = info2[1]-1
							for o in range(s2):
								current2 = info2[5+o]
								if(o+1!=s2 or hpw2%2==0): cs2 = 2
								else: cs2 = 1
								if(i==info1[4]==info2[4] and period1==period2 and info1!=info2):
									if(prof2==-1 and profSche[prof1][period1][current2]<=int(k+1/s1)*hpw1%2):
										permute = 1
									elif((cs1==cs2 or (cs1==1 and profSche[prof1][period1][current1]==1) or (cs2==1 and profSche[prof2][period2][current2]==1)) and ((profSche[prof1][period1][current2]<=0+int((k+1)/s1)*hpw1%2 and profSche[prof2][period2][current1]<=0+int((o+1)/s2)*hpw2%2) or prof1==prof2)):
										permute = 1
									else:
										permute = 0
									if(permute==1):
										new_info1 = copy.deepcopy(info1)
										new_info1[5+k] = current2
										new_info2 = copy.deepcopy(info2)
										new_info2[5+o] = current1
										cost = Cost(info1,info2,new_info1,new_info2,profSche,profSubject,profPeriod)
										neighbor = (info1,info2,new_info1,new_info2,cost)
										if(neighbor in neighborhood): pass
										else: neighborhood.append(neighbor)
										if(info1[4]!=info2[4]): print("Error! Permutation being made between different subject groups!")
										elif(info1[1]!=info2[1]): print("Error! Permutation being made between different periods!")
									else: pass
								else: pass
	'''
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
					try:
						from_slot = info[4+s] # Get the slot from which the subject will be moved
					except:
						print(info)
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
											cost = Cost(info,sbj2_info,new_info1,new_info2,profSche,profSubject,profPeriod)
											neighbor = (info,sbj2_info,new_info1,new_info2,cost)
											if(neighbor in neighborhood): pass
											else: neighborhood.append(neighbor)
											if(info[4]!=sbj2_info[4]): print("Error! Permutation being made between different subject groups!",i,info[4],sbj2_info[4])
											elif(info[1]!=sbj2_info[1]): print("Error! Permutation being made between different periods!")
											#print(info,sbj2_info,'\n',new_info1,new_info2,'\n')
										else: pass
									else: pass
	
				s -= 1
	'''		
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
							cost = Cost(info,ghost_info,new_info,new_ghost_info,profSche,profSubject,profPeriod)
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
								cost = Cost(info,info2,new_info,new_info2,profSche,profSubject,profPeriod)
								neighbor = (info,info2,new_info,new_info2,cost)
								if(neighbor in neighborhood): pass
								else: neighborhood.append(neighbor)#; print('HAHA',neighbor)
							else: pass

	return neighborhood
	
###########################################################################################
###########################################################################################	
###########################################################################################		
def Cost(orig1, orig2, move1, move2, profSche, profSubject, profPeriod):

	#from math import *
	import copy

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
				hpw = i[2]
				ohpw = j[2]
				sche = copy.deepcopy(profSche[prof])
				try:
					for k in range(3):
						sche[operiod][j[5+k]] -= 2
				except:
					if(ohpw%2==1): sche[operiod][j[4+k]] += 1
					else: pass
				try:
					for k in range(3):
						sche[period][i[5+k]] += 2
				except:
					if(hpw%2==1): sche[period][i[4+k]] -= 1
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
###########################################################################################
###########################################################################################
def Best(BestIter, rejected, T, Ti, sbjHPW, sbjGroups, sbjBook, profBook, sbjSche, profSche, profSubject, profPeriod):
	global global_lowest
	
	N = Neighborhood(sbjHPW, sbjGroups, sbjBook, profBook, sbjSche, profSche, profSubject, profPeriod)
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
		if(BestMove[0+i]==BestMove[2+i]):
			bypass += 1
		else:
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
		BestMove, BestIter = Best(BestIter, rejected, T, Ti, sbjHPW, sbjGroups, sbjBook, profBook, sbjSche, profSche, profSubject, profPeriod)

	return BestMove, BestIter

###########################################################################################
###########################################################################################
###########################################################################################
def InitialSolution(p, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs):

	import copy
	
	import assign

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

	candOrdered, sbjBook, profBook, profSche, sbjSche = assign.SubjectsToProfessors(p, candAval, profSche, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs)

	# Save initial solution
	
	sbjBook0 = copy.deepcopy(sbjBook)
	profBook0 = copy.deepcopy(profBook)
	sbjSche0 = copy.deepcopy(sbjSche)
	profSche0 = copy.deepcopy(profSche)

	return candAval, profSche, sbjBook0, profBook0, sbjSche0, profSche0, candOrdered, sbjBook, profBook, profSche, sbjSche
