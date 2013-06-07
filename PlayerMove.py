import bge

class PlayerMove:
	
	#all our initialization stuff
	def __init__(self, cont):
		#get the controller
		self.cont = cont
		
		#get the Player object
		self.oPlayer = cont.owner
		
		#get the Character controller from oPlayer
		#####DO THIS#######
		self.cPlayer = bge.constraints.getCharacter(self.oPlayer)
		
		#get the movement actuator
		self.aPlayerMotion = cont.actuators["PlayerMotion"]
	
		#get the maxSpeed, acceleration, drag and sprintFactor properties
		self.maxSpeed = self.oPlayer["maxSpeed"]
		self.acceleration = self.oPlayer["acceleration"]
		self.drag = self.oPlayer["drag"]
		self.sprintFactor = self.oPlayer["sprintFactor"]
		
		#get and set the gravity of the player
		self.cPlayer.gravity = self.oPlayer["gravity"]
		
		#get the keyboard
		self.kbd = bge.logic.keyboard
	
		#make some temporary values for the movement stuff
		self.moveX = 0.0
		self.moveY = 0.0
		
		#and values for the directional values
		self.directionValues = {'w':0.0, 'a':0.0, 's':0.0, 'd':0.0}
		self.directionKeys = {'w':bge.events.WKEY, 'a':bge.events.AKEY, 's':bge.events.SKEY, 'd':bge.events.DKEY}
		
	
	#checks if the shift key is pressed and returns the appropriate speed
	def getSpeed(self):
		#if the shift key is pressed, multiply the maxSpeed by the sprintFactor and return it
		if(self.kbd.events[bge.events.LEFTSHIFTKEY] > 0):
			return self.maxSpeed * self.sprintFactor
		#otherwise, just return the maxSpeed
		return self.maxSpeed
		
	#calculate the value of the directional speed of any given direction key
	def setDirectionVelocity(self, direction):
		#get the maxSpeed
		maxSpeed = self.getSpeed()
		#if the key is pressed, add acceleration
		if self.kbd.events[self.directionKeys[direction]] > 0:
			self.directionValues[direction] = self.directionValues[direction] + self.acceleration
			#if the value passes the maxSpeed, stop it and set it to the maxSpeed
			if self.directionValues[direction] > maxSpeed:
				self.directionValues[direction] = maxSpeed
		#if the key's released, implement drag
		else:
			self.directionValues[direction] = self.directionValues[direction] - self.drag
			#if the subtraction dropped the value into the negative, set it to 0
			if self.directionValues[direction] < 0:
				self.directionValues[direction] = 0
	
	#calculate the movement values
	def calculateMovement(self):
		self.moveX = self.directionValues['d'] - self.directionValues['a']
		self.moveY = self.directionValues['w'] - self.directionValues['s']
	
	#set up and trigger the actuators
	def activateMovement(self):
		#set the actuator to local movement
		self.aPlayerMotion.useLocalDLoc = True
		
		#set up the dLoc values
		self.aPlayerMotion.dLoc = (self.moveX, self.moveY, 0)
		
		#and activate!
		self.cont.activate(self.aPlayerMotion)
	
	#check to see if the player jumped
	def checkJump(self):
		if(self.kbd.events[bge.events.SPACEKEY] > 0):
			self.cPlayer.jump()
	
	#the main method, does all the stuff
	def update(self):
		#first set all the keys
		for key in self.directionKeys:
			self.setDirectionVelocity(key)
		
		#calculate the movement
		self.calculateMovement()
		
		#apply the movement to the actuators and activate them
		self.activateMovement()
		
		#also, jump!
		self.checkJump()

player_move = PlayerMove(bge.logic.getCurrentController())

def main():
	player_move.update()