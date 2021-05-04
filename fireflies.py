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
flashedFliesOpenSet = [] # flies that need to reset urge of neighbors
flashedFliesClosedSet = [] # flies that have already flashed and reset its urge
colorTraits = [
	[255,0,0], #red
	[0,255,0], # green
	[0,0,255], # blue
	[255,255,0], # yellow
	[255,0,255], # purple
	[0,255,255], # cyan
	[232, 30, 99], # pink
	[255, 152, 0], # orange
	[96, 125, 139], # blue gray
	[255,87,51] # blood orange
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
		self.colorTrait = colorTraits[random.randint(0,9)]
		self.hue = [0,0,0]

	def draw(self):
		self.circle.setFill('black')
		self.circle.setOutline('black')
		self.circle.draw(win)

	def compute_hue(self,colorTraits):
		if self.currentUrge < (self.threshold-30):
			self.hue = [0,0,0]
		elif self.currentUrge < (self.threshold-15):
			self.hue[0] = min(colorTraits[0],0+colorTraits[0]*(self.currentUrge - (self.threshold-30))/(30/2))
			self.hue[1] = min(colorTraits[1],0+colorTraits[1]*(self.currentUrge - (self.threshold-30))/(30/2))
			self.hue[2] = min(colorTraits[2],0+colorTraits[2]*(self.currentUrge - (self.threshold-30))/(30/2))
		else:
			self.hue[0] = max(0,colorTraits[0]-colorTraits[0]*(self.currentUrge - (self.threshold-15))/(30/2))
			self.hue[1] = max(0,colorTraits[1]-colorTraits[1]*(self.currentUrge - (self.threshold-15))/(30/2))
			self.hue[2] = max(0,colorTraits[2]-colorTraits[2]*(self.currentUrge - (self.threshold-15))/(30/2))


# As time progresses, increase urge every second

for i in range(random.randint(40,85)): # randomly generate Firefly instances at random coordinates within frame
	fireflies.append(Firefly(random.randint(fireflyRadius,windowWidth-fireflyRadius),random.randint(fireflyRadius,windowHeight-fireflyRadius)))

for fly in fireflies:
    fly.draw()

previousTime = time.time()

while not closeWindow:
	currentTime = time.time() # get currentTime in seconds
	if (currentTime-previousTime) > .1: # if one second has elapsed
		previousTime = currentTime # previous time becomes the old current time

		for fly in fireflies: # for all fireflies
			if fly.flashed:
				fly.flashed = False

			fly.compute_hue(fly.colorTrait)
			fly.circle.setFill(color_rgb(fly.hue[0],fly.hue[1],fly.hue[2]))
			fly.circle.setOutline(color_rgb(fly.hue[0],fly.hue[1],fly.hue[2]))
			fly.currentUrge += 1 # increase urge by one every one second
			win.flush()

			if fly.currentUrge >= fly.threshold: # if current urge exceeds the fireflies' threshold
				fly.flashed = True
				flashedFliesOpenSet.append(fly)
				fly.currentUrge = 0 # reset phase/currentUrge


		for flashedFly in flashedFliesOpenSet:
			# TODO: alter this loop to eliminate every visited fly to reduce iterations.
			#       Would need to reset the list of flies on the outside of the loop to ensure every fly is visitied.
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
