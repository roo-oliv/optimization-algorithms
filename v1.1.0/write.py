###########################################################################################	
###########################################################################################	
###########################################################################################	
def Variables(sbjGroups,profSubject,sbjProfs,candAval,profPeriod,sbjPeriod,sbjHPW,sbjOrdered,sbjBook,sbjBook0,profBook,profBook0,profSche,profSche0,sbjSche,sbjSche0,BestMove_log):
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
	str10 = ', '.join('{}{}'.format(key, val) for key, val in sorted(sbjBook0.items()))
	str11 = ', '.join('{}{}'.format(key, val) for key, val in sorted(profBook.items()))
	str12 = ', '.join('{}{}'.format(key, val) for key, val in sorted(profBook0.items()))
	str13 = ', '.join(str(e) for e in profSche)
	str14 = ', '.join(str(e) for e in profSche0)
	str15 = ', '.join(str(e) for e in sbjSche)
	str16 = ', '.join(str(e) for e in sbjSche0)
	str17 = ', '.join(str(e) for e in BestMove_log)
	string = 'sbjGroups:\n'+str1+'   '+str(len(sbjGroups))+'\n\n'+'profSubject:\n'+str2+'   '+str(len(profSubject))+'\n\n'+'sbjProfs:\n'+str3+'   '+str(len(sbjProfs))+'\n\n'+'candAval:\n'+str4+'   '+str(len(candAval))+'\n\n'+'profPeriod:\n'+str5+'   '+str(len(profPeriod))+'\n\n'+'sbjPeriod:\n'+str6+'   '+str(len(sbjPeriod))+'\n\n'+'sbjHPW:\n'+str7+'   '+str(len(sbjHPW))+'\n\n'+'sbjOrdered:\n'+str8+'   '+str(len(sbjOrdered))+'\n\n'+'sbjBook:\n'+str9+'   '+str(len(sbjBook))+'\n\n'+'sbjBook0:\n'+str10+'   '+str(len(sbjBook0))+'\n\n'+'profBook:\n'+str11+'   '+str(len(profBook))+'\n\n'+'profBook0:\n'+str12+'   '+str(len(profBook0))+'\n\n'+'profSche:\n'+str13+'   '+str(len(profSche))+'\n\n'+'profSche0:\n'+str14+'   '+str(len(profSche0))+'\n\n'+'sbjSche:\n'+str15+'   '+str(len(sbjSche))+'\n\n'+'sbjSche0:\n'+str16+'   '+str(len(sbjSche0))+'\n\n'+'BestMove_log:\n'+str17+'   '+str(len(BestMove_log))+'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
	f.write(string)
	
	return
