import bge

#all our initialization stuff
def init(cont):
	#get the Character controller
	cPlayer = bge.constraints.getCharacter(cont.owner)
	#get and set the gravity of the player
	cPlayer.gravity = cont.owner["gravity"]

	#make some temporary values for the movement stuff
	cont.owner["moveX"] = 0.0
	cont.owner["moveY"] = 0.0
	
	#and values for the directional values
	cont.owner["directionValues"] = {'w':0.0, 'a':0.0, 's':0.0, 'd':0.0}
	cont.owner["directionKeys"] = {'w':bge.events.WKEY, 'a':bge.events.AKEY, 's':bge.events.SKEY, 'd':bge.events.DKEY}
		
#the main method, does all the stuff
def update(cont):
	#first set all the keys
	for key in cont.owner["directionKeys"]:
		setDirectionVelocity(cont, key)
	
	#calculate the movement
	calculateMovement(cont)
	
	#apply the movement to the actuators and activate them
	aPlayerMotion = cont.actuators["PlayerMotion"]
	aPlayerMotion.useLocalDLoc = True
	aPlayerMotion.dLoc = (cont.owner["moveX"], cont.owner["moveY"], 0)
	cont.activate(aPlayerMotion)
	
	#also, jump!
	checkJump(cont)

	
#checks if the shift key is pressed and returns the appropriate speed
def getSpeed(cont):
	kbd = bge.logic.keyboard
	#if the shift key is pressed, multiply the maxSpeed by the sprintFactor and return it
	if(kbd.events[bge.events.LEFTSHIFTKEY] > 0):
		return cont.owner["maxSpeed"] * cont.owner["sprintFactor"]
	#otherwise, just return the maxSpeed
	return cont.owner["maxSpeed"]
		
#calculate the value of the directional speed of any given direction key
def setDirectionVelocity(cont, direction):
	kbd = bge.logic.keyboard
	#get the maxSpeed
	maxSpeed = getSpeed(cont)
	#if the key is pressed, add acceleration
	if kbd.events[cont.owner["directionKeys"][direction]] > 0:
		cont.owner["directionValues"][direction] = cont.owner["directionValues"][direction] + cont.owner["acceleration"]
		#if the value passes the maxSpeed, stop it and set it to the maxSpeed
		if cont.owner["directionValues"][direction] > maxSpeed:
			cont.owner["directionValues"][direction] = maxSpeed
	#if the key's released, implement drag
	else:
		cont.owner["directionValues"][direction] = cont.owner["directionValues"][direction] - cont.owner["drag"]
		#if the subtraction dropped the value into the negative, set it to 0
		if cont.owner["directionValues"][direction] < 0:
			cont.owner["directionValues"][direction] = 0
	
#calculate the movement values
def calculateMovement(cont):
	cont.owner["moveX"] = cont.owner["directionValues"]['d'] - cont.owner["directionValues"]['a']
	cont.owner["moveY"] = cont.owner["directionValues"]['w'] - cont.owner["directionValues"]['s']
	
#check to see if the player jumped
def checkJump(cont):
	kbd = bge.logic.keyboard
	cPlayer = bge.constraints.getCharacter(cont.owner)
	if(kbd.events[bge.events.SPACEKEY] > 0):
		self.cPlayer.jump()