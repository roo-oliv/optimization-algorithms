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
	y=86

	c = Canvas(master, width=1240, height=1754)
	c.pack()
	
	# Initial solution
	
	c.create_text(w/2, y, font=("Ubuntu","16", "bold"), text="Professor "+str(professor)+" schedule in initial solution")

	c.create_rectangle(x, y+30, x+124, y+48, fill="#fff", tags=("00n","init")) # Blank rectangle

	c.create_rectangle(x, y+48, x+124, y+120, fill="#fff", tags=("01n","init"))     # 
	xp = (c.coords("01n")[0]+c.coords("01n")[2])/2                                   # 8:00 am 
	yp = (c.coords("01n")[1]+c.coords("01n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="8:00 am - 10:00 am")          # 

	c.create_rectangle(x, y+120, x+124, y+192, fill="#fff", tags=("02n","init"))    # 
	xp = (c.coords("02n")[0]+c.coords("02n")[2])/2                                   # 10:00 am 
	yp = (c.coords("02n")[1]+c.coords("02n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="10:00 am - 12:00 pm")         # 

	c.create_rectangle(x, y+192, x+124, y+228, fill="#fff", tags=("03n","init"))    # 
	xp = (c.coords("03n")[0]+c.coords("03n")[2])/2                                   # 12:00 pm 
	yp = (c.coords("03n")[1]+c.coords("03n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="12:00 pm - 2:00 pm")          #

	c.create_rectangle(x, y+228, x+124, y+300, fill="#fff", tags=("04n","init"))    # 
	xp = (c.coords("04n")[0]+c.coords("04n")[2])/2                                   # 2:00 pm 
	yp = (c.coords("04n")[1]+c.coords("04n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="2:00 pm - 4:00 pm")           #

	c.create_rectangle(x, y+300, x+124, y+372, fill="#fff", tags=("05n","init"))    # 
	xp = (c.coords("05n")[0]+c.coords("05n")[2])/2                                   # 4:00 pm 
	yp = (c.coords("05n")[1]+c.coords("05n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="4:00 pm - 6:00 pm")           #

	c.create_rectangle(x, y+372, x+124, y+408, fill="#fff", tags=("06n","init"))    # 
	xp = (c.coords("06n")[0]+c.coords("06n")[2])/2                                   # 6:00 pm 
	yp = (c.coords("06n")[1]+c.coords("06n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="6:00 pm - 7:00 pm")           #

	c.create_rectangle(x, y+408, x+124, y+480, fill="#fff", tags=("07n","init"))    # 
	xp = (c.coords("07n")[0]+c.coords("07n")[2])/2                                   # 7:00 pm 
	yp = (c.coords("07n")[1]+c.coords("07n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="7:00 pm - 9:00 pm")           #

	c.create_rectangle(x, y+480, x+124, y+552, fill="#fff", tags=("08n","init"))    # 
	xp = (c.coords("08n")[0]+c.coords("08n")[2])/2                                   # 9:00 pm 
	yp = (c.coords("08n")[1]+c.coords("08n")[3])/2                                   # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="9:00 pm - 11:00 pm")          #

	week = ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday']
	for i in range(5):
		c.create_rectangle(x+124+i*186, y+30, x+310+i*186, y+48, fill="#fff")
		c.create_rectangle(x+124+i*186, y+48, x+310+i*186, y+120, fill="#fff", tags=("00,0"+str(2*i),"init"))
		c.create_rectangle(x+124+i*186, y+120, x+310+i*186, y+192, fill="#fff", tags=("00,0"+str(2*i+1),"init"))
		c.create_rectangle(x+124+i*186, y+192, x+310+i*186, y+228, fill="#fff")
		c.create_rectangle(x+124+i*186, y+228, x+310+i*186, y+300, fill="#fff", tags=("01,0"+str(2*i),"init"))
		c.create_rectangle(x+124+i*186, y+300, x+310+i*186, y+372, fill="#fff", tags=("01,0"+str(2*i+1),"init"))
		c.create_rectangle(x+124+i*186, y+372, x+310+i*186, y+408, fill="#fff")
		c.create_rectangle(x+124+i*186, y+408, x+310+i*186, y+480, fill="#fff", tags=("02,0"+str(2*i),"init"))
		c.create_rectangle(x+124+i*186, y+480, x+310+i*186, y+552, fill="#fff", tags=("02,0"+str(2*i+1),"init"))
		c.create_text(x+217+i*186, y+39, font=("Arial","12"), text=week[i])

	halfSlots = []
	for i in range(len(solution.profBook0[professor])):
		for j in range(5,len(solution.profBook0[professor][i])):
			
			sbj = solution.profBook0[professor][i][0]
			slot = solution.profBook0[professor][i][j]
			
			if(j+1==len(solution.profBook0[professor][i]) and solution.profBook0[professor][i][2]%2==1):
				
				coord = c.coords("0"+str(solution.profBook0[professor][i][1]-1)+",0"+str(slot))
				coord = [int(i) for i in coord]
				if("0"+str(solution.profBook0[professor][i][1]-1)+",0"+str(slot) in halfSlots):
					c.create_rectangle((coord[0]+coord[2])/2, coord[1], coord[2], coord[3], fill="#ccc")
					c.create_text((coord[0]+3*coord[2])/4,(coord[1]+coord[3])/2, font=("Ubuntu","15"), justify=CENTER, text="Subject "+str(sbj))
				else:
					c.create_rectangle(coord[0], coord[1], (coord[0]+coord[2])/2, coord[3], fill="#ccc")
					halfSlots.append("0"+str(solution.profBook0[professor][i][1]-1)+",0"+str(slot))
					c.create_text((3*coord[0]+coord[2])/4,(coord[1]+coord[3])/2, font=("Ubuntu","15"), justify=CENTER, text="Subject "+str(sbj))
			else:
			
				coord = c.coords("0"+str(solution.profBook0[professor][i][1]-1)+",0"+str(slot))
				coord = [int(i) for i in coord]
				c.create_rectangle(coord[0], coord[1], coord[2], coord[3], fill="#ccc")
				c.create_text((coord[0]+coord[2])/2,(coord[1]+coord[3])/2, font=("Ubuntu","15"), justify=CENTER, text="Subject "+str(sbj))

	# Tabu Search solution
	
	y += h/2
	
	c.create_text(w/2, y, font=("Ubuntu","16", "bold"), text="Professor "+str(professor)+" schedule in Tabu Search solution")

	c.create_rectangle(x, y+30, x+124, y+48, fill="#fff", tag="0n") # Blank rectangle

	c.create_rectangle(x, y+48, x+124, y+120, fill="#fff", tag="1n")       # 
	xp = (c.coords("1n")[0]+c.coords("1n")[2])/2                           # 8:00 am 
	yp = (c.coords("1n")[1]+c.coords("1n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="8:00 am - 10:00 am")  # 

	c.create_rectangle(x, y+120, x+124, y+192, fill="#fff", tag="2n")      # 
	xp = (c.coords("2n")[0]+c.coords("2n")[2])/2                           # 10:00 am 
	yp = (c.coords("2n")[1]+c.coords("2n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="10:00 am - 12:00 pm") # 

	c.create_rectangle(x, y+192, x+124, y+228, fill="#fff", tag="3n")      # 
	xp = (c.coords("3n")[0]+c.coords("3n")[2])/2                           # 12:00 pm 
	yp = (c.coords("3n")[1]+c.coords("3n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="12:00 pm - 2:00 pm")  #

	c.create_rectangle(x, y+228, x+124, y+300, fill="#fff", tag="4n")      # 
	xp = (c.coords("4n")[0]+c.coords("4n")[2])/2                           # 2:00 pm 
	yp = (c.coords("4n")[1]+c.coords("4n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="2:00 pm - 4:00 pm")   #

	c.create_rectangle(x, y+300, x+124, y+372, fill="#fff", tag="5n")      # 
	xp = (c.coords("5n")[0]+c.coords("5n")[2])/2                           # 4:00 pm 
	yp = (c.coords("5n")[1]+c.coords("5n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="4:00 pm - 6:00 pm")   #

	c.create_rectangle(x, y+372, x+124, y+408, fill="#fff", tag="6n")      # 
	xp = (c.coords("6n")[0]+c.coords("6n")[2])/2                           # 6:00 pm 
	yp = (c.coords("6n")[1]+c.coords("6n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="6:00 pm - 7:00 pm")   #

	c.create_rectangle(x, y+408, x+124, y+480, fill="#fff", tag="7n")      # 
	xp = (c.coords("7n")[0]+c.coords("7n")[2])/2                           # 7:00 pm 
	yp = (c.coords("7n")[1]+c.coords("7n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="7:00 pm - 9:00 pm")   #

	c.create_rectangle(x, y+480, x+124, y+552, fill="#fff", tag="8n")      # 
	xp = (c.coords("8n")[0]+c.coords("8n")[2])/2                           # 9:00 pm 
	yp = (c.coords("8n")[1]+c.coords("8n")[3])/2                           # rectangle
	c.create_text(xp, yp, font=("Arial","12"), text="9:00 pm - 11:00 pm")  #

	week = ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday']
	for i in range(5):
		c.create_rectangle(x+124+i*186, y+30, x+310+i*186, y+48, fill="#fff")
		c.create_rectangle(x+124+i*186, y+48, x+310+i*186, y+120, fill="#fff", tag="0,"+str(2*i))
		c.create_rectangle(x+124+i*186, y+120, x+310+i*186, y+192, fill="#fff", tag="0,"+str(2*i+1))
		c.create_rectangle(x+124+i*186, y+192, x+310+i*186, y+228, fill="#fff")
		c.create_rectangle(x+124+i*186, y+228, x+310+i*186, y+300, fill="#fff", tag="1,"+str(2*i))
		c.create_rectangle(x+124+i*186, y+300, x+310+i*186, y+372, fill="#fff", tag="1,"+str(2*i+1))
		c.create_rectangle(x+124+i*186, y+372, x+310+i*186, y+408, fill="#fff")
		c.create_rectangle(x+124+i*186, y+408, x+310+i*186, y+480, fill="#fff", tag="2,"+str(2*i))
		c.create_rectangle(x+124+i*186, y+480, x+310+i*186, y+552, fill="#fff", tag="2,"+str(2*i+1))
		c.create_text(x+217+i*186, y+39, font=("Arial","12"), text=week[i])

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
	
	c.update()
	c.postscript(file = "professor_"+str(professor)+"_schedule.ps", pageheight="29.70c",x="0",y="0",height="1754",width="1240") 

os.system("convert -density 300 *.ps  schedules.pdf")
os.system("find . -name \*.ps -type f -delete")
