from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import pink, green, brown, white, black

c = canvas.Canvas("report.pdf")
for i in range(12):
	c.setFillColorRGB(235/255,241/255,222/255)
	c.setStrokeColorRGB(196/255,215/255,155/255)
	c.rect(70,700-i*44,470,22,stroke=1,fill=1)
	c.setFillColorRGB(1,1,1)
	c.rect(70,678-i*44,470,22,stroke=1,fill=1)

c.setFillColor(black)
c.setFont("Times-Roman",8)
c.drawString(80,707,"Subject 0")

c.save()
