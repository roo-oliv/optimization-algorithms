import tabu_search as solution
from tkinter import *
import os

master = Tk()

w=1240
h=1754
m=120

c = Canvas(master, width=1240, height=1754)
c.pack()

c.create_rectangle(0, 0, w, h, fill="#fff", outline="#fff")

c.create_rectangle(m, 60, w-m, 180, fill="#9bbb59", outline="#cadba6")
c.create_text(m+60, 90, fill="#fff", font=("Ubuntu","12", "bold") , text="SUBJECT")
c.create_text(m+170, 90, fill="#fff", font=("Ubuntu","12", "bold") , text="CLASS")
c.create_text(m+420, 90, fill="#fff", font=("Ubuntu","12", "bold") , text="SCHEDULE")
c.create_text(m+720, 90, fill="#fff", font=("Ubuntu","12", "bold") , text="PROFESSOR")
c.create_text(m+920, 90, fill="#fff", font=("Ubuntu","12", "bold") , text="OFFERED AS")	

for i in range(13):
	c.create_rectangle(m, m+120*i, w-m, m+120*i+60, fill="#ebf1de", outline="#cadba6")
	c.create_rectangle(m, m+120*i+60, w-m, m+120*i+120, fill="#fff", outline="#cadba6")

count = -1
page = 0
for i in solution.sbjBook:
	if(i == -1):
		pass
	else:
		classroom = -1
		sameSche = [[],[],[]]
		scheRecord = [[],[],[]]
		for j in range(len(solution.sbjBook[i])):
			classroom += 1
			count += 1
			period = solution.sbjBook[i][j][1]-1
			hpw = solution.sbjBook[i][j][2]
			professor = solution.sbjBook[i][j][3]
			group = solution.sbjBook[i][j][4]
			if(group==None):
				group = 'Elective'
			else:
				course_id = int(group/5)
				b26 = ''
				d = int(1)
				while(d<course_id):
					d = int(d*26)
				if(d>=26):d = int(d/26)
				else: pass
				while(d>=1):
					b26 = b26+chr(int(course_id/d) + ord('A'))
					course_id = course_id % d
					d = d/26
				group = str(group+1)+'-Year required subject\nfor course '+b26
			sche = solution.sbjBook[i][j][5:]
		
			if(sche in scheRecord[period]):
				class_id = scheRecord[period].index(sche)
				class_idBK = scheRecord[period].index(sche)
				sameSche[period][class_id][0] += 1
			else:
				scheRecord[period].append(sche)
				sameSche[period].append([0])
				class_id = scheRecord[period].index(sche)
				class_idBK = scheRecord[period].index(sche)
			
			schedule = ""
			for k in sche:
				if(schedule==""):pass
				else: schedule = schedule + "\n"
				
				weekday = int((k+1)/2) + (k+1)%2
				if(weekday==1): weekday = 'Monday '
				elif(weekday==2): weekday = 'Tuesday '
				elif(weekday==3): weekday = 'Wednesday '
				elif(weekday==4): weekday = 'Thursday '
				else: weekday = 'Friday '
				
				if(k%2==0 and period==0): hour = "from 8:00 am to 10:00 am"
				elif(k%2==0 and period==1): hour = "from 2:00 pm to 4:00 pm"
				elif(k%2==0 and period==2): hour = "from 7:00 pm to 9:00 pm"
				elif(k%2==1 and period==0): hour = "from 10:00 am to 12:00 pm"
				elif(k%2==1 and period==1): hour = "from 4:00 pm to 6:00 pm"
				elif(k%2==1 and period==2): hour = "from 9:00 pm to 11:00 pm"
			
				schedule = schedule + weekday + hour
			
			b26 = ''
			div = int(1)
			while(div<class_id):
				div = int(div*26)
			if(div>=26):div = int(div/26)
			else: pass
			while(div>=1):
				b26 = b26+chr(int(class_id/div) + ord('A'))
				class_id = class_id % div
				div = div/26
		
			if(period==0): periodTX = " - morning"
			elif(period==1): periodTX = " - afternoon"
			else: periodTX = " - evening"
		
			if(count<=25): pass
			else:
				c.update()
				c.postscript(file = "classes-"+str(page)+".ps", pageheight="29.70c",x="0",y="0",height="1754",width="1240") 
				c.delete("lines")
				count = 0
				page += 1
				
			c.create_text(m+60, 150+60*count, fill="#000", font=("Ubuntu","10") , text=i, tags="lines") # Subject
			c.create_text(m+170, 150+60*count, fill="#000", font=("Ubuntu","10") , text=b26+str(sameSche[period][class_idBK][0]+1)+periodTX, tags="lines") # Class
			c.create_text(m+420, 150+60*count, fill="#000", font=("Ubuntu","10") , text=schedule, tags="lines") # Schedule
			c.create_text(m+720, 150+60*count, fill="#000", font=("Ubuntu","10") , text=professor, tags="lines") # Professor
			c.create_text(m+920, 150+60*count, fill="#000", font=("Ubuntu","10") , justify=CENTER, text=group, tags="lines") # Group

c.update()
c.postscript(file = "classes-"+str(page)+".ps", pageheight="29.70c",x="0",y="0",height="1754",width="1240") 

#Concatenate PS files and output a single PDF, then clear PS files
os.system("convert -density 300 *.ps  classes.pdf")
os.system("find . -name \*.ps -type f -delete")


#mainloop()

