import sys, pygame
import numpy as np
import wave
from time import sleep
from math import *

pygame.init()
size = width, height = 1024, 600
stepAdjust = 0.05
# 1024 x 600 screen, 100px on the sides, 100px on the bottom
# the waveform will then be in a 824 * 500 rectangle
waveOffX = 400
waveOffY = 100
waveWidth = width - (waveOffX)
waveHeight = height - waveOffY

black = 30, 30, 30
white = 255, 252, 251

screen = pygame.display.set_mode(size)
screen.fill(white)
#pygame.display.setCaption('drum machine')
clock = pygame.time.Clock()
fontBig = pygame.font.Font("Helvetica-Bold.ttf", 26)

class Sample:
	
	numSegments = 200
	thickness = waveWidth/numSegments
	"""
	filename
	name
	start: between 0.0 and 1.0
	end: between 0.0 and 1.0
	attack:
	decay:
	"""
	
	
	def populateRects(self):
		#self.sampleLength = int(len(self.signal) * (self.end - self.start))
		self.sampleIt = int(ceil(len(self.signal)/self.numSegments))
	
	
		self.rects = []

		#for x in xrange (0,len(self.signal), self.sampleIt):
		for x in xrange (0,200):
			self.rects.append(np.mean(abs(self.signal[x*self.sampleIt:((x + 1)*self.sampleIt)])))
		
		self.highest = max(self.rects)	
		
		for d in xrange(0,len(self.rects)):
			self.rects[d] = self.rects[d]/ self.highest
		
		self.rectSegment = self.rects
		
	def updateRects(self):
	
	# def updateRects(self):
		self.sampleLength = (len(self.signal) * (self.end - self.start))
		self.sampleIt = int(self.sampleLength/self.numSegments)
	
	
		self.rectSegment = []
		for x in xrange (int(self.start*len(self.signal)),int(self.end*len(self.signal)), self.sampleIt):
			self.rectSegment.append(np.mean(abs(self.signal[x:(x+self.sampleIt)])) / self.highest)
		#for x in xrange (int(self.start * len(self.signal)),int(self.end * len(self.signal)), self.sampleIt):
		#	self.rectSegment.append(np.mean(abs(self.signal[x:(x + self.sampleIt)])) / self.highest)
		
		# highest = max(self.rects)	
		
		# for d in xrange(0,len(self.rects)):
			# self.rects[d] = self.rects[d]/ highest
			
	def setName(self, name):
		self.name = name
	
	def setFileName(self, filename):
		self.filename = filename
		#write to preset file
		#send midi to change bank
		
	# The following functions send midi and update the display
	def setStart(self, start):
		if (start > 1 or start >= self.end - stepAdjust):
			self.start = self.end - stepAdjust
		elif (start < 0):
			self.start = 0
		else:
			self.start = start
		
		self.updateRects()
		
	def setEnd(self, end):
		if (end < 0 or end <= self.start + stepAdjust):
			self.end = self.start + stepAdjust
		elif (end > 1):
			self.end = 1
		else:
			self.end = end
		
		self.updateRects()
		
	def setAttack(self, attack):
		self.attack = attack
		
	def setDecay(self, decay):
		self.decay = decay
		
	def setSustain(self, sustain):
		self.sustain = sustain
		
	def setRelease(self, release):
		self.release = release
	
	def getThickness(self):
		return self.thickness
	
	
	def getRects(self):
		return self.rects
		
	def __init__(self, name, filename):
		self.start = 0.0
		self.end = 1.0
		self.attack = 0
		self.decay = 25
		self.release = 10
		self.sustain = 63
		
		
		self.rects = []
		self.name = name
		self.filename = filename
		
		
		spf = wave.open(filename, 'r')
		self.signal  = spf.readframes(-1)
		self.signal = np.fromstring(self.signal, 'Int16')#[::4]
		self.timeLength = spf.getnframes() / float(spf.getframerate())
		print spf.getnframes()
		print spf.getframerate()
		#self.sampleLength = len(self.signal)
		#self.sampleIt = int(sampleLength/numSegments)
		self.populateRects()
		#write to preset file
		#send midi to change bank

def main():
	crashed = False
	started = False
	g = 0.0
	samp2 = Sample('vdub', 'vdub.wav')
	samp1 = Sample('g11', 'g11.wav')
	while not crashed:
		
		if not started:
			sampleView(samp1, True)
			started = True
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					samp1.setStart(samp1.start + stepAdjust)
					
				if event.key == pygame.K_LEFT:
					samp1.setStart(samp1.start - stepAdjust)
					
				if event.key == pygame.K_RIGHTBRACKET:
					samp1.setEnd(samp1.end + stepAdjust)
					
				if event.key == pygame.K_LEFTBRACKET:
					samp1.setEnd(samp1.end - stepAdjust)
					
				if event.key == pygame.K_DOWN:
					temp = samp1
					samp1 = samp2
					samp2 = temp
					
				sampleView(samp1, False)
				print samp1.start
			
		#samp1.setStart(g)
		#samp1.setEnd(g + .2)
		#samp1.setStart(0.2)
		
			#print(event)
			
			
		
		pygame.display.flip()
		#clock.tick(10)

	pygame.quit()
	
	quit()
	
	
def sampleView(sample, init):
	#print sample.filename
	lengthS = "" + str(sample.timeLength) + "s"
	sampleText = fontBig.render(lengthS, True, (black))
	currentFilename = fontBig.render(sample.filename, True, (black))
	
	
	done = 0
	
	
	if init:
		while not done:
			screen.fill(white)
			screen.blit(currentFilename, (200,50))
			screen.blit(sampleText, (450,50))
			for d in xrange(0, len(sample.rectSegment)):
		
				pygame.draw.rect(screen, black, ((d * sample.thickness) + (waveOffX/2), (220 - ((sample.rectSegment[d]*200)/2)),2, sample.rectSegment[d] * 200))
				
				sleep(.001)
				pygame.display.flip()
			done = 1
			
	else:
		while not done:
			screen.fill(white)
			screen.blit(currentFilename, (200,50))
			screen.blit(sampleText, (450,50))
			for d in xrange(0, len(sample.rectSegment)):
		
				pygame.draw.rect(screen, black, ((d * sample.thickness) + (waveOffX/2), (220 - ((sample.rectSegment[d]*200)/2)),2, sample.rectSegment[d] * 200))
				
			done = 1
		
	return 1
	
main()

