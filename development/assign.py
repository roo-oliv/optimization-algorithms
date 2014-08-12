###########################################################################################	
###########################################################################################	
###########################################################################################	
def SubjectsToProfessors(p, candAval, profSche, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs):

	import get
	import copy

	# Declare global variables
	global candOrdered
	global sbjBook
	global profBook
	global profPos
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
				test_hpw = 0
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
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor, profPos, force = get.Professor(sbj,candidates,period,profPos,candOrdered,profPeriod, force)
							info = [sbj,period,hpw,professor,i,slot]
							if(profSche[professor][period-1][slot]==0):
								profSche[professor][period-1][slot] += 2; test_hpw += 2
								sbjSche[sbj][period-1][slot] += 2
								gotProf = 1
								if(hpw!=test_hpw): raise Exception("Bad slot allocation")
								else: pass
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
							for k in range(8,-9,-1):
								if(9>=a+k+mod>=0 and k+mod!=0 and slots[period-1][a+k+mod]<2):
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
							try: slots[period-1][b-control]; cond1 = 1
							except: cond1 = 0
							if(control%2==1 and b-control!=a and cond1==1 and slots[period-1][b-control]<2):
								b -= control
								try:
									if(b<0 and b+1+control!=a and slots[period-1][b+1+control]<2): control += 1; b += control
								except:
									control += 1; b += control
							elif(b+control<=9 and b+control!=a and slots[period-1][b+control]<2):
								b += control
							elif(b>9 and b-1-control!=a and slots[period-1][b-1-control]<2): control += 1; b -= control
							else: pass
							if(waste==0 and not(0<=b<=9) and a!=5 and slots[period-1][5]<2):
								b = 5
								control = 0
								waste = 1
							else:
								alloc2 = -1
								print('ALLOC ERROR 1 in alloc2, ',hpw,period,'\n',slots)
					if(alloc==-1 or alloc2==-1):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor, profPos, force = get.Professor(sbj,candidates,period,profPos,candOrdered,profPeriod, force)
							info = [sbj,period,hpw,professor,i,slot,slot2]
							if(profSche[professor][period-1][slot]==0 and profSche[professor][period-1][slot2]<2):
								profSche[professor][period-1][slot] += 2; test_hpw += 2
								profSche[professor][period-1][slot2] += 1; test_hpw += 1
								sbjSche[sbj][period-1][slot] += 2
								sbjSche[sbj][period-1][slot2] += 1
								gotProf = 1
								if(hpw!=test_hpw): raise Exception("Bad slot allocation")
								else: pass
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
							for k in range(8,-9,-1):
								if(9>=a+k+mod>=0 and k+mod!=0 and slots[period-1][a+k+mod]==0):
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
							if(control%2==1 and b-control!=a and slots[period-1][b-control]==0):
								b -= control
								if(b<0 and b+1+control!=a and slots[period-1][b+1+control]==0): control += 1; b += control
							elif(b+control<=9 and b+control!=a and slots[period-1][b+control]==0):
								b += control
							elif(b>9 and b-1-control!=a and slots[period-1][b-1-control]==0): control += 1; b -= control
							else: pass
							if(waste==0 and not(0<=b<=9) and a!=5 and slots[period-1][5]==0):
								b = 5
								control = 0
								waste = 1
							elif(waste==1 and not(0<=b<=9)):
								alloc2 = -1
					if(alloc==-1 or alloc2==-1):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor, profPos, force = get.Professor(sbj,candidates,period,profPos,candOrdered,profPeriod,force)
							info = [sbj,period,hpw,professor,i,slot,slot2]
							if(profSche[professor][period-1][slot]==0 and profSche[professor][period-1][slot2]==0):
								profSche[professor][period-1][slot] += 2; test_hpw += 2
								profSche[professor][period-1][slot2] += 2; test_hpw += 2
								sbjSche[sbj][period-1][slot] += 2
								sbjSche[sbj][period-1][slot2] += 2
								gotProf = 1
								if(hpw!=test_hpw): raise Exception("Bad slot allocation")
								else: pass
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
							for k in range(8,-9,-1):
								if(9>=a+k+mod>=0 and k+mod!=0 and slots[period-1][a+k+mod]==0):
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
							if(control%2==1 and b-control!=a and slots[period-1][b-control]==0):
								b -= control
								if(b<0 and b+1+control!=a and slots[period-1][b+1+control]==0): control += 1; b += control
							elif(b+control<=9 and b+control!=a and slots[period-1][b+control]==0):
								b += control
							elif(b>9 and b-1-control!=a and slots[period-1][b-1-control]==0): control += 1; b -= control
							else: pass
							if(waste==0 and not(0<=b<=9) and a!=5 and slots[period-1][5]==0):
								b = 5
								control = 0
								waste = 1
							else:
								alloc2 = -1
								print('ALLOC ERROR 2 in alloc2, ',hpw,period,'\n',slots)
					while(alloc3==0):
						if(c_mod==0):
							if(a%2==0 and a+1<=9 and a+1!=b and slots[period-1][a+1]<2): c = a+1
							elif(a-1>=0 and a-1!=b and slots[period-1][a-1]<2): c = a-1
							else: pass
						elif(c_mod==1):
							if(a%2==0 and b+1<=9 and b+1!=a and slots[period-1][b+1]<2): c = b+1
							elif(b-1>=0 and b-1!=a and slots[period-1][b-1]<2): c = b-1
							else:pass
						elif(c_mod==2 and 0!=a and 0!=b and slots[period-1][0]<2):
							c = 0
						else: c_mod -= 1
						c_mod += 1
						#print(str(a)+", "+str(b)+", "+str(c))
						if(slots[period-1][c]==1 and waste==0):
							slot3 = c
							slots[period-1][c] += 1
							alloc3 = 1
						elif(slots[period-1][c]==0 and waste==1):
							slot3 = c
							slots[period-1][c] += 1
							alloc3 = 1
						else:
							c += 1
							try:
								while(c+1==a or c+1==b and slots[period-1][c+1]<2):
									c += 1
							except:
								c = 10
						if(c==10 and (waste==0 and c_mod>2) and 0!=a and 0!=b):
							c = 0
							waste = 1
						elif(c==10 and (waste==1 and c_mod>2)):
							alloc3 = -1
						else: waste = 1
					if(alloc==-1 or (alloc2==-1 or alloc3==-1)):
						print('Allocation ERROR!',hpw,period,alloc,alloc2,alloc3)
						print(slots)
					else:
						gotProf = 0
						while(gotProf==0):
							t+=1
							professor, profPos, force = get.Professor(sbj,candidates,period,profPos,candOrdered,profPeriod,force)
							info = [sbj,period,hpw,professor,i,slot,slot2,slot3]
							if(profSche[professor][period-1][slot]==0 and (profSche[professor][period-1][slot2]==0 and profSche[professor][period-1][slot3]<2)):
								profSche[professor][period-1][slot] += 2; test_hpw += 2
								profSche[professor][period-1][slot2] += 2; test_hpw += 2
								profSche[professor][period-1][slot3] += 1; test_hpw += 1
								sbjSche[sbj][period-1][slot] += 2
								sbjSche[sbj][period-1][slot2] += 2
								sbjSche[sbj][period-1][slot3] += 1
								gotProf = 1
								if(hpw!=test_hpw): raise Exception("Bad slot allocation")
								else: pass
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
				
				hpw_diff = 0
				for k in profBook[professor]:
					hpw_diff += k[2]
				for k in range(3):
					for l in range(10):
						hpw_diff -= profSche[professor][k][l]
				if(hpw_diff!=0): print(hpw_diff); raise Exception("profBook and profSche divergence found")
				else: pass
				
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

				print('Professor %i was assigned to teach subject %i on' % (info[3],info[0]),week_message1,hour_message1,week_message2,hour_message2,week_message3,hour_message3,'\b.')
				
				if(sbj!=info[0]): print('ERROR 001')

				repeat -= 1
				if(repeat==0): period = 1
				
		for j in range(3):
			for k in range(10):
				if(slots[j][k]<2):
					sbj = -1
					professor = -1
					info = [sbj,j+1,2-slots[j][k],professor,i,k]
					
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
				else: pass
		
#-----------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------#

	for i in range(len(sbjGroups)): # iterate for all subject groups
	#for i in range(0): # iterate for all subject groups
		for j in range(5): # each group is composed by 5 subjects
			abort = 0
			#slots2 = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
			#sbj = sbjGroups[i][j] # obtain the current subject number
			candidates = list(candAval[j+5*i])
			candOrdered = sorted(candidates, key=lambda item: item[0], reverse=True)
			#hpw = sbjHPW[sbj] # get the hours per week for this subject
			#period = sbjPeriod[sbj]
			profPos = 0
			profSche_temp = copy.deepcopy(profSche)
			sbjBook_temp = copy.deepcopy(sbjBook)
			profBook_temp = copy.deepcopy(profBook)
			
			for oinfo in sbjBook[sbjGroups[i][j]]:
				gotProf = 0
				if(oinfo[0]==-1): pass
				else:
					sbj = oinfo[0]
					if(sbj==-1): raise Exception('What the fuck?!')
					hpw = oinfo[2]
					period = oinfo[1]
					t = 0
					while(gotProf==0):
						t += 1
						professor, profPos, force = get.Professor(sbj,candidates,period,profPos,candOrdered,profPeriod,force)
						schedule = profSche[professor][period-1]
						if(hpw==2):
							slot1 = oinfo[5]-2*(oinfo[5]%2)+1
							info = [sbj,period,hpw,professor,i,slot1]
							if(schedule[slot1]==0):
								profSche_temp[professor][period-1][slot1] += 2
								gotProf = 1
							else: profPos += 1
							if(info[0]==-1): raise Exception('What the fuck?!')
						elif(hpw==3):
							slot1 = oinfo[5]-2*(oinfo[5]%2)+1
							slot2 = oinfo[6]-2*(oinfo[6]%2)+1
							info = [sbj,period,hpw,professor,i,slot1,slot2]
							if(schedule[slot1]==0 and schedule[slot2]<2 ):
								profSche_temp[professor][period-1][slot1] += 2
								profSche_temp[professor][period-1][slot2] += 1
								gotProf = 1
							else: profPos += 1
							if(info[0]==-1): raise Exception('What the fuck?!')
						elif(hpw==4):
							slot1 = oinfo[5]-2*(oinfo[5]%2)+1
							slot2 = oinfo[6]-2*(oinfo[6]%2)+1
							info = [sbj,period,hpw,professor,i,slot1,slot2]
							if(schedule[slot1]==0 and schedule[slot2]==0 ):
								profSche_temp[professor][period-1][slot1] += 2
								profSche_temp[professor][period-1][slot2] += 2
								gotProf = 1
							else: profPos += 1
							if(info[0]==-1): raise Exception('What the fuck?!')
						else:
							slot1 = oinfo[5]-2*(oinfo[5]%2)+1
							slot2 = oinfo[6]-2*(oinfo[6]%2)+1
							slot3 = oinfo[7]-2*(oinfo[7]%2)+1
							info = [sbj,period,hpw,professor,i,slot1,slot2,slot3]
							if(schedule[slot1]==0 and schedule[slot2]==0 and schedule[slot3]<2):
								profSche_temp[professor][period-1][slot1] += 2
								profSche_temp[professor][period-1][slot2] += 2
								profSche_temp[professor][period-1][slot3] += 1
								gotProf = 1
							else: profPos += 1
							if(info[0]==-1): raise Exception('What the fuck?!')
					
						if(t>len(candidates)**2):
							gotProf = -1
							abort = 1
						else: pass
						
						if(info[0]==-1): raise Exception('What the fuck?!')
		
		
			# mod -> 0: just one period; 1: morning and night
			#if(period==1): repeat = 1
			#else: repeat = 0
			#while(repeat>=0):
			#	alloc = 0
			#	if(repeat==1 and period==1): period = 3
			#	else: pass
			#	# Get the slots that will be occupied
			#	t = 0
			#	count = 0
			#	for k in range(10): #sbjSche[sbj][period-1]:
			#		#original = slots[period-1][k]
			#		original = sbjSche[sbj][period-1][k]
			#		if(original!=0):
			#			count += 1
			#			if(count==1):
			#				if(k%2==0):
			#					slot = k+1
			#					slots2[period-1][slot] = original
			#				else:
			#					slot = k-1
			#					slots2[period-1][slot] = original
			#			elif(count==2):
			#				if(k%2==0):
			#					slot2 = k+1
			#					slots2[period-1][slot2] = original
			#				else:
			#					slot2 = k-1
			#					slots2[period-1][slot2] = original
			#			else:
			#				if(k%2==0):
			#					slot3 = k+1
			#					slots2[period-1][slot3] = original
			#				else:
			#					slot3 = k-1
			#					slots2[period-1][slot3] = original
			#			if(count>3): print('ERROR!!!')
			#			gotProf = 0
			#			while(gotProf==0):
			#				t+=1
			#				professor, profPos, force = get.Professor(sbj,candidates,period,profPos,candOrdered,profPeriod,force)
			#				if(hpw==2 and count==1):
			#					info = [sbj,period,hpw,professor,i,slot]
			#				elif(2<hpw<5 and count==2):
			#					info = [sbj,period,hpw,professor,i,slot,slot2]
			#				elif(hpw==5 and count==3):
			#					info = [sbj,period,hpw,professor,i,slot,slot2,slot3]
			#				else: pass
			#				if(profSche[professor][period-1][slot]==0):
			#					profSche_temp[professor][period-1][slot] += 2
			#					gotProf = 1
			#				else: profPos += 1
			#				if(t>len(candidates)**2):
			#					gotProf = -1
			#					abort = 1
			#				else: pass
			#			
			#		else: pass
					
					if(info[0]==-1): print(sbj); print(oinfo); print(info); raise Exception("Unexisting subject allocated")
					
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

					print('Professor %i was assigned to teach subject %i on' % (info[3],info[0]),week_message1,hour_message1,week_message2,hour_message2,week_message3,hour_message3,'\b.')
		
					if(sbj!=info[0]): print('ERROR 002')
			
					#repeat -= 1
					#if(repeat==0): period = 1
			
			for j in range(3):
				for k in range(10):
					if(slots[j][k]<2):
						sbj = -1
						professor = -1
						info = [sbj,j+1,2-slots[j][k],professor,i,k]
						
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
				profSche = copy.deepcopy(profSche_temp)
				sbjBook = copy.deepcopy(sbjBook_temp)
				profBook = copy.deepcopy(profBook_temp)
			else: pass
			
			hpw_diff = 0
			for k in profBook[professor]:
				if(k[3]!=-1):
					hpw_diff += k[2]
			for k in range(3):
				for l in range(10):
					hpw_diff -= profSche[professor][k][l]
			if(hpw_diff!=0): print(hpw_diff); raise Exception("profBook and profSche divergence found")
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
		cycle = 0
		while(prof_hpw<8):
			test_hpw = 0
			try: sbj = profSubject[i][attempt]
			except:
				if(cycle==0):
					cycle = 1
					attempt = 0
					invert = 2
					sbj = profSubject[i][0]
				else:
					prof_hpw=20
					print('Unable to assign as many classes as required to professor '+str(i))
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
				profSche[i][period-1][a] += 2; test_hpw += 2
				sbjSche[sbj][period-1][a] += 2
				prof_hpw += 2
				valid = 1
				if(hpw!=test_hpw): raise Exception("Bad slot allocation")
				else: pass
				
			elif(hpw==3 and a!=None):
				try: b = pref_slots1[0]
				except: 
					if(a%2==0): mod = 1
					else: mod = -1
					for j in range(8,-9,-1):
						if(9>=a+j+mod>=0 and schedule[a+j+mod]<2 and ((a+j+mod in pref_slots0) or (a+j+mod in pref_slots1)) and j+mod!=0):
							b = a+j+mod
							break
					else:
						for j in range(8,-9,-1):
							if(9>=a+j+mod>=0 and schedule[a+j+mod]<2 and j+mod!=0):
								b = a+j+mod
								break
				
				if(b!=None):	
					info = [sbj,period,hpw,i,group,a,b]
					profSche[i][period-1][a] += 2; test_hpw += 2
					sbjSche[sbj][period-1][a] += 2
					profSche[i][period-1][b] += 1; test_hpw += 1
					sbjSche[sbj][period-1][b] += 1
					prof_hpw += 3
					valid = 1
					if(hpw!=test_hpw): raise Exception("Bad slot allocation")
					else: pass
				else: valid = 0
				
			elif(hpw==4 and a!=None):
				if(a%2==0): mod = 1
				else: mod = -1
				for j in range(8,-9,-1):
					if(9>=a+j+mod>=0 and schedule[a+j+mod]==0 and ((a+j+mod in pref_slots0) or (a+j+mod in pref_slots1)) and j+mod!=0):
						b = a+j+mod
						break
				else:
					for j in range(8,-9,-1):
						if(9>=a+j+mod>=0 and schedule[a+j+mod]==0 and j+mod!=0):
							b = a+j+mod
							break
				if(b!=None):
					info = [sbj,period,hpw,i,group,a,b]
					profSche[i][period-1][a] += 2; test_hpw += 2
					sbjSche[sbj][period-1][a] += 2
					profSche[i][period-1][b] += 2; test_hpw += 2
					sbjSche[sbj][period-1][b] += 2
					prof_hpw += 4
					valid = 1
					if(hpw!=test_hpw): raise Exception("Bad slot allocation")
					else: pass
				else: valid = 0
				
			elif(hpw==5 and a!=None):
				if(a%2==0): mod = 1
				else: mod = -1
				
				for j in range(8,-9,-1):
					if(9>=a+j+mod>=0 and schedule[a+j+mod]==0 and ((a+j+mod in pref_slots0) or (a+j+mod in pref_slots1)) and j+mod!=0):
						b = a+j+mod
						break
				else:
					for j in range(8,-9,-1):
						if(9>=a+j+mod>=0 and schedule[a+j+mod]==0 and j+mod!=0):
							b = a+j+mod
							break
				if(b==None): print(schedule); print(j); print(mod); print(a)
				
				if(b%2==0): mod2 = 1
				else: mod2 = -1
				
				if(schedule[a+mod]<2 and mod!=0 and a+mod!=b): c = a+mod
				elif(schedule[b+mod2]<2 and mod2!=0 and b+mod2!=a): c = b+mod2
				else:
					for j in range(10):
						if(schedule[j]<2 and j!=a and j!=b):
							c = j
							break
						else: pass
				if(b!=None and c!=None):
					info = [sbj,period,hpw,i,group,a,b,c]
					profSche[i][period-1][a] += 2; test_hpw += 2
					sbjSche[sbj][period-1][a] += 2
					profSche[i][period-1][b] += 2; test_hpw += 2
					sbjSche[sbj][period-1][b] += 2
					profSche[i][period-1][c] += 1; test_hpw += 1
					sbjSche[sbj][period-1][c] += 1
					prof_hpw += 5
					valid = 1
					if(hpw!=test_hpw): raise Exception("Bad slot allocation")
					else: pass
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
				
				hpw_diff = 0
				for k in profBook[i]:
					hpw_diff += k[2]
				for k in range(3):
					for l in range(10):
						hpw_diff -= profSche[i][k][l]
				if(hpw_diff!=0): print('hpw_diff: '+str(hpw_diff)); raise Exception("profBook and profSche divergence found")
				else: pass
			
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

				print('Professor %i was assigned to teach subject %i on' % (info[3],info[0]),week_message1,hour_message1,week_message2,hour_message2,week_message3,hour_message3,'\b.')
			
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
	
	return candOrdered, sbjBook, profBook, profSche, sbjSche

###########################################################################################	
###########################################################################################	
###########################################################################################	
def SubjectsToProfessors_refactored(p, candAval, profSche, profPeriod, profSubject, sbjPeriod, sbjHPW, sbjOrdered, sbjGroups, sbjProfs):

	import get
	import copy
	from random import choice

	# Declare global variables
	global candOrdered
	global sbjBook
	global profBook
	global profPos
	# Create empty lists and dictionaries
	candOrdered = []
	sbjBook = {}
	profBook = {}
	
	print('\n')

# Assign professors for subject groups ( Classes A )

	for i in range(len(sbjGroups)): # iterate for all subject groups
		slots = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
		for j in range(5): # each group is composed by 5 subjects
			sbj = sbjGroups[i][j] # obtaining the current subject number
			candidates = list(candAval[j+5*i])
			candOrdered = sorted(candidates, key=lambda item: item[0], reverse=True)
			hpw = sbjHPW[sbj] # getting hours per week for this subject
			period = sbjPeriod[sbj]

			if(period==1): periods = [0,2]
			else: periods = [1]
			for period in periods:
				profPos = 0
				force = 0
				next_candidate = 1
				ignore_hpw = 0
				while(next_candidate==1):
		
					allocated = 0
					allocated_slots = []
					if(len(candOrdered)==profPos):
						ignore_hpw = 1
						profPos = 0
					professor, profPos, force = get.Professor(sbj, candidates, period, profPos, candOrdered, profPeriod, force)
					prof_hpw = 0
					try:
						for j in profBook[professor]:
							prof_hpw += j[2]
					except: pass
					if(prof_hpw < 8 or ignore_hpw == 1):
						for k in range(int((hpw+1)/2)):
							if(k==int((hpw+1)/2)-1 and hpw%2==1): requirement = 1
							else: requirement = 2
							for l in range(10):
								if(profSche[professor][period][l]+requirement <= 2 and slots[period][l]+requirement <= 2 and l not in allocated_slots):
									allocated_slots.append(l)
									allocated += 1
									break
								else: pass
						if(allocated==int((hpw+1)/2)): next_candidate = 0
						else: profPos += 1
					else: profPos += 1
								
				info = [sbj,period,hpw,professor,i]
				message = []
				days = ("Mondays ","Tuesdays ","Wednesdays ","Thursdays ","Fridays ")
				hours = ("from 8:00 am to 10:00 am", "from 10:00 am to 12:00 pm",
					 "from 2:00 pm to 4:00 pm" , "from 4:00 pm to 6:00 pm"  ,
					 "from 7:00 pm to 9:00 pm" , "from 9:00 pm to 11:00 pm" )
				for slot in allocated_slots:
					info.append(slot)
					message.append(days[int((slot-slot%2)/2)]+hours[int(2*(info[1])+slot%2)])
				for k in (6,7):
					try:
						info[k]
						try:
							info[k+1]
							message[k-6] = message[k-6]+", on"
						except: message[k-6] = message[k-6]+" and on"
					except:
						message.append('\b')
					
				#print('Professor %i was assigned to teach subject %i on' % (professor,sbj),message[0],message[1],message[2],'\b.')
				
				for k in range(len(info[5:])):
					slot = info[5+k]
					if(hpw%2 == 1 and k+6 == len(info)):
						profSche[professor][period][slot] += 1
					else:
						profSche[professor][period][slot] += 2
				
				try: sbjBook[sbj].append(info)
				except: sbjBook[sbj] = [info]
				
				try: profBook[professor].append(info)
				except: profBook[professor] = [info]
				
				hpw_diff = 0
				for k in profBook[professor]:
					hpw_diff += k[2]
				for k in range(3):
					for l in range(10):
						hpw_diff -= profSche[professor][k][l]
				if(hpw_diff!=0): print(hpw_diff); raise Exception("profBook and profSche divergence found")
				else: pass
				
				if(sbj!=info[0]): print('ERROR 001')
				
		for j in range(3):
			for k in range(10):
				if(slots[j][k]<2):
					sbj = -1
					professor = -1
					info = [sbj,j+1,2-slots[j][k],professor,i,k]
					
					try: sbjBook[sbj].append(info)
					except: sbjBook[sbj] = [info]

					try: profBook[professor].append(info)
					except: profBook[professor] = [info]
					
				else: pass
				
# Assign professors for alternate schedules in subject groups ( Classes B )
				
	for i in range(len(sbjGroups)): # iterate for all subject groups
		slots = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
		A_Classes = copy.deepcopy(sbjBook)
		for j in range(5): # each group is composed by 5 subjects
			sbj = sbjGroups[i][j] # obtaining the current subject number
			candidates = list(candAval[j+5*i])
			candOrdered = sorted(candidates, key=lambda item: item[0], reverse=True)
			hpw = sbjHPW[sbj] # getting hours per week for this subject
			period = sbjPeriod[sbj]
			
			if(period==1): periods = [0,2]
			else: periods = [1]
			for period in periods:
				for A_info in A_Classes[sbj]:
					if(A_info[1]==period):
						A_slots = A_info[5:]
				profPos = 0
				force = 0
				next_candidate = 1
				ignore_hpw = 0
				while(next_candidate==1):
		
					allocated = 0
					allocated_slots = []
					if(len(candOrdered)==profPos):
						ignore_hpw = 1
						profPos = 0
					professor, profPos, force = get.Professor(sbj, candidates, period, profPos, candOrdered, profPeriod, force)
					prof_hpw = 0
					try:
						for j in profBook[professor]:
							prof_hpw += j[2]
					except: pass
					if(prof_hpw < 8 or ignore_hpw == 1):
						for k in range(int((hpw+1)/2)):
							if(k==int((hpw+1)/2)-1 and hpw%2==1): requirement = 1
							else: requirement = 2
							for l in range(10):
								if(profSche[professor][period][l]+requirement <= 2 and slots[period][l]+requirement <= 2 and l not in allocated_slots and l not in A_slots):
									allocated_slots.append(l)
									allocated += 1
									break
								else: pass
						if(allocated==int((hpw+1)/2)): next_candidate = 0
						else: profPos += 1
					else: profPos += 1
								
				info = [sbj,period,hpw,professor,i]
				message = []
				days = ("Mondays ","Tuesdays ","Wednesdays ","Thursdays ","Fridays ")
				hours = ("from 8:00 am to 10:00 am", "from 10:00 am to 12:00 pm",
					 "from 2:00 pm to 4:00 pm" , "from 4:00 pm to 6:00 pm"  ,
					 "from 7:00 pm to 9:00 pm" , "from 9:00 pm to 11:00 pm" )
				for slot in allocated_slots:
					info.append(slot)
					message.append(days[int((slot-slot%2)/2)]+hours[int(2*(info[1])+slot%2)])
				for k in (6,7):
					try:
						info[k]
						try:
							info[k+1]
							message[k-6] = message[k-6]+", on"
						except: message[k-6] = message[k-6]+" and on"
					except:
						message.append('\b')
					
				#print('Professor %i was assigned to teach subject %i on' % (professor,sbj),message[0],message[1],message[2],'\b.')
				
				for k in range(len(info[5:])):
					slot = info[5+k]
					if(hpw%2 == 1 and k+6 == len(info)):
						profSche[professor][period][slot] += 1
					else:
						profSche[professor][period][slot] += 2
				
				try: sbjBook[sbj].append(info)
				except: sbjBook[sbj] = [info]
				
				try: profBook[professor].append(info)
				except: profBook[professor] = [info]
				
				hpw_diff = 0
				for k in profBook[professor]:
					hpw_diff += k[2]
				for k in range(3):
					for l in range(10):
						hpw_diff -= profSche[professor][k][l]
				if(hpw_diff!=0): print(hpw_diff); raise Exception("profBook and profSche divergence found")
				else: pass
				
				if(sbj!=info[0]): print('ERROR 001')
				
		for j in range(3):
			for k in range(10):
				if(slots[j][k]<2):
					sbj = -1
					professor = -1
					info = [sbj,j+1,2-slots[j][k],professor,i,k]
					
					try: sbjBook[sbj].append(info)
					except: sbjBook[sbj] = [info]

					try: profBook[professor].append(info)
					except: profBook[professor] = [info]
					
				else: pass

# Assign professors to subjects not constrained to subject groups

	for professor in range(p):
		prof_hpw = 0
		try:
			for info in profBook[professor]:
				prof_hpw += info[2]
		except: pass
		while(prof_hpw < 8):
			sbj = choice((profSubject[professor][0], profSubject[professor][0], profSubject[professor][0],
				      profSubject[professor][0], profSubject[professor][1], profSubject[professor][1],
				      profSubject[professor][1], profSubject[professor][2], profSubject[professor][2], 
				      profSubject[professor][3])) 							# choosing one subject for this professor
			hpw = sbjHPW[sbj] # getting hours per week for this subject
			possible_periods = []
			for period in range(len(profPeriod[professor])):
				if(profPeriod[professor][period]==2): possible_periods.append(period)
				else: pass
			period = choice(possible_periods)
			
			for group in range(len(sbjGroups)):
				if(sbj in sbjGroups[group]): break
				else: pass
			else: group = None
			info = [sbj,period,hpw,professor,group]
			allocated_slots = []
			for i in range(int(hpw/2)+hpw%2):
				if(hpw%2 == 1 and i == int(hpw/2)+hpw%2): requirement = 1
				else: requirement = 2
				for j in range(10):
					if(profSche[professor][period][j]+requirement <= 2 and not j in allocated_slots):
						allocated_slots.append(j)
						break
					else: pass
				else:
					raise Exception("Professor %i has too many subjects. Please, lower the minimum of hours per week a professor must teach." % (professor))
			
			prof_hpw += hpw
			
			message = []
			days = ("Mondays ","Tuesdays ","Wednesdays ","Thursdays ","Fridays ")
			hours = ("from 8:00 am to 10:00 am", "from 10:00 am to 12:00 pm",
				 "from 2:00 pm to 4:00 pm" , "from 4:00 pm to 6:00 pm"  ,
				 "from 7:00 pm to 9:00 pm" , "from 9:00 pm to 11:00 pm" )
			for slot in allocated_slots:
				info.append(slot)
				message.append(days[int((slot-slot%2)/2)]+hours[int(2*(info[1])+slot%2)])
			
			for k in (6,7):
				try:
					info[k]
					try:
						info[k+1]
						message[k-6] = message[k-6]+", on"
					except: message[k-6] = message[k-6]+" and on"
				except:
					message.append('\b')
			#print('Professor %i was assigned to teach subject %i on' % (professor,sbj),message[0],message[1],message[2],'\b.')
			
			for k in range(len(info[5:])):
				slot = info[5+k]
				if(hpw%2 == 1 and k+6 == len(info)):
					profSche[professor][period][slot] += 1
				else:
					profSche[professor][period][slot] += 2
			
			try: sbjBook[sbj].append(info)
			except: sbjBook[sbj] = [info]
			
			try: profBook[professor].append(info)
			except: profBook[professor] = [info]
			
			hpw_diff = 0
			for k in profBook[professor]:
				hpw_diff += k[2]
			for k in range(3):
				for l in range(10):
					hpw_diff -= profSche[professor][k][l]
			if(hpw_diff!=0): print(hpw_diff,"\n",profBook[professor],"\n",profSche[professor]); raise Exception("profBook and profSche divergence found")
			else: pass
			
			if(sbj!=info[0]): print('ERROR 001')
	return candOrdered, sbjBook, profBook, profSche


