from graphics import *
import math
import random

windowWidth = 400
windowHeight = 400
fireflyRadius = 3

win = GraphWin("Fireflies",windowWidth,windowHeight,autoflush=False)
win.setBackground('black')
closeWindow = False
fireflies = []

def distbetween(start,end):
	return math.sqrt((start.x-end.x)**2+(start.y-end.y)**2)


class Firefly():
	def __init__(self,i,j):
		self.x = i
		self.y = j
		self.radius = fireflyRadius
		self.currentUrge = random.randint(0,100)
		self.threshold = 100
		self.circle = Circle(Point(self.x,self.y),self.radius)
		self.flashed = False
		self.hue = [0,0,0]

	def draw(self):
		self.circle.setFill('black')
		self.circle.setOutline('black')
		self.circle.draw(win)

	def compute_hue(self):
		if self.currentUrge < (self.threshold-30):
			self.hue = [0,0,0]
		elif self.currentUrge < (self.threshold-15):
			self.hue[0] = min(255,0+255*(self.currentUrge - (self.threshold-30))/(30/2))
			self.hue[1] = min(255,0+255*(self.currentUrge - (self.threshold-30))/(30/2))
		else:
			self.hue[0] = max(0,255-255*(self.currentUrge - (self.threshold-15))/(30/2))
			self.hue[1] = max(0,255-255*(self.currentUrge - (self.threshold-15))/(30/2))


# As time progresses, increase urge every second

for i in range(random.randint(60,70)): # randomly generate Firefly instances at random coordinates within frame
	fireflies.append(Firefly(random.randint(fireflyRadius,windowWidth-fireflyRadius),random.randint(fireflyRadius,windowHeight-fireflyRadius)))
	#fireflies.append(Firefly(random.randint(200, 250),random.randint(200,250)))

for fly in fireflies:
    fly.draw()

previousTime = 0

while not closeWindow:
	currentTime = int(time.time()*1000) # get currentTime in seconds
	if (currentTime-previousTime) >= 80: # if one second has elapsed
		previousTime = currentTime # previous time becomes the old current time

		for fly in fireflies: # for all fireflies
			if fly.flashed:
				fly.flashed = False

			fly.compute_hue()
			fly.circle.setFill(color_rgb(fly.hue[0],fly.hue[1],fly.hue[2]))
			fly.currentUrge += 1 # increase urge by one every one second
			win.flush()

			if fly.currentUrge >= fly.threshold: # if current urge exceeds the fireflies' threshold
				fly.flashed = True
				fly.currentUrge = 0 # reset phase/currentUrge

		for fly1 in fireflies:
			if fly1.flashed == True:
				for fly2 in fireflies:
					if distbetween(fly1,fly2) <= 100 and (fly2 != fly1) and fly2.currentUrge < fly2.threshold:
						fly2.currentUrge = 0

	if win.checkKey():
	    closeWindow = True


win.getMouse()
