###########################################################################################	
###########################################################################################	
###########################################################################################	
def TabuSearch(Itermax, sbjHPW, sbjGroup, sbjBook, profBook, profSche, profSubject, profPeriod):

	import get
	
	BestMove_log = []
	Iter = 0 
	BestIter = 0
	T = []
	Ti = []
	
	while(Iter-BestIter<Itermax):
		Iter += 1
		BestMove,BestIter = get.Best(BestIter, [], T, Ti, sbjHPW, sbjGroup, sbjBook, profBook, profSche, profSubject, profPeriod)
		
		BestMove_log.append(BestMove)
		
		# Update current solution with the movement picked
		pS1 = profSche[BestMove[0][3]]
		pS2 = profSche[BestMove[1][3]]
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
		period1 = BestMove[2][1]
		operiod1 = BestMove[0][1]
		period2 = BestMove[3][1]
		operiod2 = BestMove[1][1]
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
		                          
			# Update profBook
		try:
			profBook[prof1].remove(BestMove[0])
			profBook[prof1].append(BestMove[2])
		except:
			print(profBook[prof1])
			print(BestMove)
			raise
		try:
			if(prof2!=-1):
				profBook[prof2].remove(BestMove[1])
				profBook[prof2].append(BestMove[3])
			else: pass
		except:
			print(profBook[prof2])
			print(BestMove)
			raise
			# Update sbjBook
		sbjBook[osbj1].remove(BestMove[0])
		sbjBook[sbj1].append(BestMove[2])
		if(osbj2!=-1):
			sbjBook[osbj2].remove(BestMove[1])
			sbjBook[sbj2].append(BestMove[3])
		else: pass

	return sbjBook, profBook, profSche, BestMove_log
