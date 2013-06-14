import bge
import math
import mathutils


def update(cont):
	mouseLook(cont)
	playerMove(cont)

def mouseLook(cont):
	#get the PlayerMotion and CamMotion actuator
	aPlayerMotion = cont.actuators["PlayerMotion"]
	aCamMotion = cont.actuators["CamMotion"]
	
	#get the mouse offset
	mouseOffset = getMouseOffset(cont)
	
	#First we make sure we're using local rotation
	aPlayerMotion.useLocalDRot = True
	
	#Next, apply the x value of the mouse to the Z rotation of Player
	aPlayerMotion.dRot = [0, 0, -mouseOffset[0]]
	
	#make sure the pitch isn't outside the limits
	pitchLimit(cont, mouseOffset[1])
	
	#make the rotation matrix and apply it to the camera
	cont.owner["playerCam"].localOrientation = mathutils.Matrix.Rotation(math.radians(cont.owner["camRotation"]), 3, 'X')
	
	#Actuate the actuators
	cont.activate(aPlayerMotion)

def playerMove(cont):
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

def init(cont):
	#----
	#PlayerMove init
	#----
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
	
	#----
	#MouseLook init
	#----
	
	#get the PlayerCam object
	for obj in cont.owner.children:
		if type(obj) == bge.types.KX_Camera:
			cont.owner["playerCam"] = obj
	
	#the initial pitch of the camera
	cont.owner["camRotation"] = 90.0
	
	#center the mouse from the get-go so it doesn't skip around anywhere at all
	bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))


#this returns the change in mouse position
def getMouseOffset(cont):
	#the mouse
	mouse = bge.logic.mouse
	
	#Get the normalized mouse position
	#
	#This takes the mouse.position values, multiplies them by 2 and subtracts 1
	#so you get a value between -1 and 1 on the X and Y axis
	mousePosition = (mouse.position[0] * 2 - 1, mouse.position[1] * 2 - 1)
	
	#check the deadzones
	#if mouse.position falls within a deadzone value, mousePosition gets 0.0 assigned to that axis
	mx = 0.0 if (abs(mousePosition[0]) < cont.owner["deadzoneX"]) else (mousePosition[0] * cont.owner["rotXspeed"])
	my = 0.0 if (abs(mousePosition[1]) < cont.owner["deadzoneY"]) else (mousePosition[1] * cont.owner["rotYspeed"])
	
	#center the mouse to the screen/window
	#
	#If we don't center the mouse to the screen rotation mayhem will occur
	bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))
	
	#return the mouse offset
	return (mx, my)
		
#rotation limiter
def pitchLimit(cont,mouseOffset):
	#the camera has it's own rotation property, so let's add mousePosition[1] to that
	cont.owner["camRotation"] += mouseOffset * -cont.owner["rotYspeed"]
	#next, make sure the rotation doesn't go outside the max and min defined in Player
	if cont.owner["camRotation"] > cont.owner["rotMax"]:
		cont.owner["camRotation"] = cont.owner["rotMax"]
	if cont.owner["camRotation"] < cont.owner["rotMin"]:
		cont.owner["camRotation"] = cont.owner["rotMin"]
		
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
		cPlayer.jump()
