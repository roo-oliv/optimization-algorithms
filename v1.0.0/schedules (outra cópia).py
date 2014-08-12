import tabu_search as solution
from tkinter import *
import os

mod = 1
try: solution.profBook[-1]
except: mod = 0
for professor in (range(len(solution.profBook)-mod)):
	master = Tk()

	w=1240
	h=1754
	x=86

	c = Canvas(master, width=1240, height=1754)
	c.pack()

	c.create_text(w/2, x, font=("Ubuntu","16", "bold"), text="Professor "+str(professor)+" schedule")

	c.create_rectangle(x, x+30, x+124, x+48, fill="#fff", tag="0n") # Blank rectangle

	c.create_rectangle(x, x+48, x+124, x+120, fill="#fff", tag="1n")       # 
	xp = (c.coords("1n")[0]+c.coords("1n")[2])/2                           # 8:00 am 
	yp = (c.coords("1n")[1]+c.coords("1n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="8:00 am - 10:00 am")  # 

	c.create_rectangle(x, x+120, x+124, x+192, fill="#fff", tag="2n")      # 
	xp = (c.coords("2n")[0]+c.coords("2n")[2])/2                           # 10:00 am 
	yp = (c.coords("2n")[1]+c.coords("2n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="10:00 am - 12:00 pm") # 

	c.create_rectangle(x, x+192, x+124, x+228, fill="#fff", tag="3n")      # 
	xp = (c.coords("3n")[0]+c.coords("3n")[2])/2                           # 12:00 pm 
	yp = (c.coords("3n")[1]+c.coords("3n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="12:00 pm - 2:00 pm")  #

	c.create_rectangle(x, x+228, x+124, x+300, fill="#fff", tag="4n")      # 
	xp = (c.coords("4n")[0]+c.coords("4n")[2])/2                           # 2:00 pm 
	yp = (c.coords("4n")[1]+c.coords("4n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="2:00 pm - 4:00 pm")   #

	c.create_rectangle(x, x+300, x+124, x+372, fill="#fff", tag="5n")      # 
	xp = (c.coords("5n")[0]+c.coords("5n")[2])/2                           # 4:00 pm 
	yp = (c.coords("5n")[1]+c.coords("5n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="4:00 pm - 6:00 pm")   #

	c.create_rectangle(x, x+372, x+124, x+408, fill="#fff", tag="6n")      # 
	xp = (c.coords("6n")[0]+c.coords("6n")[2])/2                           # 6:00 pm 
	yp = (c.coords("6n")[1]+c.coords("6n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="6:00 pm - 7:00 pm")   #

	c.create_rectangle(x, x+408, x+124, x+480, fill="#fff", tag="7n")      # 
	xp = (c.coords("7n")[0]+c.coords("7n")[2])/2                           # 7:00 pm 
	yp = (c.coords("7n")[1]+c.coords("7n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="7:00 pm - 9:00 pm")   #

	c.create_rectangle(x, x+480, x+124, x+552, fill="#fff", tag="8n")      # 
	xp = (c.coords("8n")[0]+c.coords("8n")[2])/2                           # 9:00 pm 
	yp = (c.coords("8n")[1]+c.coords("8n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="9:00 pm - 11:00 pm")  #

	week = ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday']
	for i in range(5):
		c.create_rectangle(x+124+i*186, x+30, x+310+i*186, x+48, fill="#fff")
		c.create_rectangle(x+124+i*186, x+48, x+310+i*186, x+120, fill="#fff", tag="0,"+str(2*i))
		c.create_rectangle(x+124+i*186, x+120, x+310+i*186, x+192, fill="#fff", tag="0,"+str(2*i+1))
		c.create_rectangle(x+124+i*186, x+192, x+310+i*186, x+228, fill="#fff")
		c.create_rectangle(x+124+i*186, x+228, x+310+i*186, x+300, fill="#fff", tag="1,"+str(2*i))
		c.create_rectangle(x+124+i*186, x+300, x+310+i*186, x+372, fill="#fff", tag="1,"+str(2*i+1))
		c.create_rectangle(x+124+i*186, x+372, x+310+i*186, x+408, fill="#fff")
		c.create_rectangle(x+124+i*186, x+408, x+310+i*186, x+480, fill="#fff", tag="2,"+str(2*i))
		c.create_rectangle(x+124+i*186, x+480, x+310+i*186, x+552, fill="#fff", tag="2,"+str(2*i+1))
		c.create_text(x+217+i*186, x+39, font=("Arial","12"), text=week[i])

	halfSlots = []
	for i in range(len(solution.profBook[professor])):
		for j in range(5,len(solution.profBook[professor][i])):
			
			sbj = solution.profBook[professor][i][0]
			slot = solution.profBook[professor][i][j]
			
			if(j+1==len(solution.profBook[professor][i]) and solution.profBook[professor][i][2]%2==1):
				
				coord = c.coords(str(solution.profBook[professor][i][1]-1)+","+str(slot))
				coord = [int(i) for i in coord]
				if(str(solution.profBook[professor][i][1]-1)+","+str(slot) in halfSlots):
					c.create_rectangle((coord[0]+coord[2])/2, coord[1], coord[2], coord[3], fill="#ccc")
					c.create_text((coord[0]+3*coord[2])/4,(coord[1]+coord[3])/2, font=("Ubuntu","15"), justify=CENTER, text="Subject "+str(sbj))
				else:
					c.create_rectangle(coord[0], coord[1], (coord[0]+coord[2])/2, coord[3], fill="#ccc")
					halfSlots.append(str(solution.profBook[professor][i][1]-1)+","+str(slot))
					c.create_text((3*coord[0]+coord[2])/4,(coord[1]+coord[3])/2, font=("Ubuntu","15"), justify=CENTER, text="Subject "+str(sbj))
			else:
			
				coord = c.coords(str(solution.profBook[professor][i][1]-1)+","+str(slot))
				coord = [int(i) for i in coord]
				c.create_rectangle(coord[0], coord[1], coord[2], coord[3], fill="#ccc")
				c.create_text((coord[0]+coord[2])/2,(coord[1]+coord[3])/2, font=("Ubuntu","15"), justify=CENTER, text="Subject "+str(sbj))
				
	
	c.create_text(x+400,x+800, font=("Arial","12"),text=str(solution.profSche[professor]))
	
	c.update()
	c.postscript(file = "professor_"+str(professor)+"_schedule.ps", pageheight="29.70c",x="0",y="0",height="1754",width="1240") 

os.system("convert -density 300 *.ps  schedules.pdf")
os.system("find . -name \*.ps -type f -delete")
