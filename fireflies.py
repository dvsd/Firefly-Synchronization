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
flashedFliesOpenSet = []
flashedFliesClosedSet = []
colorTraits = [
	[255,0,0],
	[0,255,0],
	[0,0,255],
	[255,255,0],
	[255,0,255]
]

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
		self.colorTrait = colorTraits[random.randint(0,4)]
		self.hue = [0,0,0]

	def draw(self):
		self.circle.setFill('black')
		self.circle.setOutline('black')
		self.circle.draw(win)

	def compute_hue(self,colorTraits):
		if self.currentUrge < (self.threshold-30):
			self.hue = [0,0,0]
		elif self.currentUrge < (self.threshold-15):
			#self.hue[0] = min(255,0+255*(self.currentUrge - (self.threshold-30))/(30/2))
			self.hue[0] = min(colorTraits[0],0+colorTraits[0]*(self.currentUrge - (self.threshold-30))/(30/2))
			self.hue[1] = min(colorTraits[1],0+colorTraits[1]*(self.currentUrge - (self.threshold-30))/(30/2))
			self.hue[2] = min(colorTraits[2],0+colorTraits[2]*(self.currentUrge - (self.threshold-30))/(30/2))
		else:
			#self.hue[0] = max(0,255-255*(self.currentUrge - (self.threshold-15))/(30/2))
			self.hue[0] = max(0,colorTraits[0]-colorTraits[0]*(self.currentUrge - (self.threshold-15))/(30/2))
			self.hue[1] = max(0,colorTraits[1]-colorTraits[1]*(self.currentUrge - (self.threshold-15))/(30/2))
			self.hue[2] = max(0,colorTraits[2]-colorTraits[2]*(self.currentUrge - (self.threshold-15))/(30/2))
			#self.hue[1] = max(0,255-255*(self.currentUrge - (self.threshold-15))/(30/2))


# As time progresses, increase urge every second

for i in range(random.randint(40,85)): # randomly generate Firefly instances at random coordinates within frame
	fireflies.append(Firefly(random.randint(fireflyRadius,windowWidth-fireflyRadius),random.randint(fireflyRadius,windowHeight-fireflyRadius)))
	#fireflies.append(Firefly(random.randint(100, 250),random.randint(100,250)))

for fly in fireflies:
    fly.draw()

previousTime = time.time()

while not closeWindow:
	currentTime = time.time() # get currentTime in seconds
	#print(currentTime)
	#print(previousTime)
	if (currentTime-previousTime) > .1: # if one second has elapsed
		previousTime = currentTime # previous time becomes the old current time

		for fly in fireflies: # for all fireflies
			if fly.flashed:
				fly.flashed = False

			fly.compute_hue(fly.colorTrait)
			fly.circle.setFill(color_rgb(fly.hue[0],fly.hue[1],fly.hue[2]))
			fly.circle.setOutline(color_rgb(fly.hue[0],fly.hue[1],fly.hue[2]))
			#fly.circle.setFill(color_rgb(fly.colorTrait[0],fly.colorTrait[1],fly.colorTrait[2]))
			#fly.circle.setOutline(color_rgb(fly.colorTrait[0],fly.colorTrait[1],fly.colorTrait[2]))
			fly.currentUrge += 1 # increase urge by one every one second
			win.flush()

			if fly.currentUrge >= fly.threshold: # if current urge exceeds the fireflies' threshold
				fly.flashed = True
				flashedFliesOpenSet.append(fly)
				fly.currentUrge = 0 # reset phase/currentUrge

		#for fly1 in fireflies:
		#	if fly1.flashed == True:
		#		for fly2 in fireflies:
		#			if distbetween(fly1,fly2) <= 100 and (fly2 != fly1) and fly2.currentUrge < fly2.threshold and fly2.currentUrge != 0:
		#				fly2.currentUrge = 0

		for flashedFly in flashedFliesOpenSet:
			for fly in fireflies:
				if fly not in flashedFliesOpenSet and fly not in flashedFliesClosedSet:
					if distbetween(flashedFly,fly) <= 50 and (flashedFly!= fly) and fly.currentUrge < fly.threshold and fly.currentUrge != 0:
						fly.currentUrge = 0
						fly.colorTrait = flashedFly.colorTrait
						flashedFliesOpenSet.append(fly)
			flashedFliesOpenSet.remove(flashedFly)
			flashedFliesClosedSet.append(flashedFly)

	if win.checkKey():
	    closeWindow = True


win.getMouse()
