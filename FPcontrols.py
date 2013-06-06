#
#	Script: First Person Player control script
#	Code: Chris Langford
#	Creation Date: 2013.05.18
#

#import yonder BGE
import bge
import mathutils
import math

#Rotation of the Player and PlayerCam objects is controlled by the mouse
#Player rotates around its Z axis, while PlayerCam rotates around it's X axis
#PlayerCam is parented to Player, so when Player rotates PlayerCam rotates with it

def mouseLook(cont):

	#initialization stuff
	if not "playerInit" in cont.owner:
		#get the Player object
		oPlayer = cont.owner

		#get the PlayerCam object
		for obj in oPlayer.children:
			if obj["objName"] == "PlayerCam":
				oPlayerCam = obj
		
		#get the PlayerMotion and CamMotion actuators
		aPlayerMotion = cont.actuators["PlayerMotion"]
		aCamMotion = cont.actuators["CamMotion"]
		#get the mouse
		mouse = bge.logic.mouse
		
		#get any custom properties
		deadzoneX = oPlayer["deadzoneX"]
		deadzoneY = oPlayer["deadzoneY"]
		rotXspeed = oPlayer["rotXspeed"]
		rotYspeed = oPlayer["rotYspeed"]
		rotMin = oPlayer["rotMin"]
		rotMax = oPlayer["rotMax"]
		
		#center the mouse from the get-go so it doesn't skip around anywhere at all
		bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))

		oPlayer["init"] = True
	
	


	
	#Get the normalized mouse position
	#
	#This takes the mouse.position values, multiplies them by 2 and subtracts 1
	#so you get a value between -1 and 1 on the X and Y axis
	mousePosition = (mouse.position[0] * 2 - 1, mouse.position[1] * 2 - 1)
	
	#check the deadzones
	#if mouse.position falls within a deadzone value, mousePosition gets 0.0 assigned to that axis
	if(abs(mousePosition[0]) < deadzoneX):
		mx = 0.0
	else:
		mx = mousePosition[0] * rotXspeed
	if(abs(mousePosition[1]) < deadzoneY):
		my = 0.0
	else:
		my = mousePosition[1] * rotYspeed
	mousePosition = (mx, my)
	
	#center the mouse to the screen/window
	#
	#If we don't center the mouse to the screen rotation mayhem will occur
	bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))
	
	#apply the rotation to Player and PlayerCam
	#
	#This is where those actuators come in handy
	#First we make sure we're using local rotation
	aPlayerMotion.useLocalDRot = True
	
	#Next, apply the x value of the mouse to the Z rotation of Player
	aPlayerMotion.dRot = [0, 0, -mousePosition[0]]
	
	#PlayerCam rotation uses some freaky scary matrix stuff
	#This allows for precise control of the min and max rotation on the camera's local X axis
	#
	#the camera has it's own rotation property, so let's add mousePosition[1] to that
	oPlayerCam["rotation"] += mousePosition[1] * -rotYspeed
	#next, make sure the rotation doesn't go outside the max and min defined in Player
	if oPlayerCam["rotation"] > rotMax:
		oPlayerCam["rotation"] = rotMax
	if oPlayerCam["rotation"] < rotMin:
		oPlayerCam["rotation"] = rotMin
	
	#make the rotation matrix and apply it to the camera
	oPlayerCam.localOrientation = mathutils.Matrix.Rotation(math.radians(oPlayerCam["rotation"]), 3, 'X')
	
	#Actuate the actuators
	cont.activate(aPlayerMotion)



#
#player movement
#
def playerMove(cont):
	#get Player
	oPlayer = cont.owner
	
	#get the movement actuator
	aPlayerMotion = cont.actuators["PlayerMotion"]
	
	#get the maxSpeed, acceleration and drag properties
	maxSpeed = oPlayer["maxSpeed"]
	acceleration = oPlayer["acceleration"]
	drag = oPlayer["drag"]
	
	#get the keyboard
	kbd = bge.logic.keyboard
	
	#make some temporary values for the movement stuff
	moveX = 0.0
	moveY = 0.0
	
	#we've got some values we only want to declare on startup, so we'll do a little initialization trickery to do so
	#THERE'S PROBABLY A BETTER WAY TO DO THIS
	if not 'moveInit' in oPlayer:
		oPlayer['moveInit'] = True
		oPlayer['w'] = 0.0
		oPlayer['a'] = 0.0
		oPlayer['s'] = 0.0
		oPlayer['d'] = 0.0
	
	#let's see what keys are pressed on the keyboard
	#
	
	#let's implement a "sprint" mode that multiplies the final movement values by sprintFactor
	if(kbd.events[bge.events.LEFTSHIFTKEY] > 0):
		maxSpeed *= oPlayer["sprintFactor"]
	else:
		maxSpeed = oPlayer["maxSpeed"]
	#we're also going to apply the acceleration and drag values to each of these values 
	#depending on whether the key is pressed or not
	if(kbd.events[bge.events.WKEY] > 0):
		oPlayer['w'] += acceleration
		#make sure w isn't higher than the maxSpeed
		if oPlayer['w'] > maxSpeed:
			oPlayer['w'] = maxSpeed
	#and now for the drag
	else:
		oPlayer['w'] -= drag
		#we don't want to overdo it (e.g. go backwards) so make sure it doesn't drop below 0
		if oPlayer['w'] < 0:
			oPlayer['w'] = 0 
	
	#repeat for the other keys
	if(kbd.events[bge.events.AKEY] > 0):
		oPlayer['a'] += acceleration
		if oPlayer['a'] > maxSpeed:
			oPlayer['a'] = maxSpeed
	else:
		oPlayer['a'] -= drag
		if oPlayer['a'] < 0:
			oPlayer['a'] = 0
	
	if(kbd.events[bge.events.SKEY] > 0):
		oPlayer['s'] += acceleration
		if oPlayer['s'] > maxSpeed:
			oPlayer['s'] = maxSpeed
	else:
		oPlayer['s'] -= drag
		if oPlayer['s'] < 0:
			oPlayer['s'] = 0
	
	if(kbd.events[bge.events.DKEY] > 0):
		oPlayer['d'] += acceleration
		if oPlayer['d'] > maxSpeed:
			oPlayer['d'] = maxSpeed
	else:
		oPlayer['d'] -= drag
		if oPlayer['d'] < 0:
			oPlayer['d'] = 0
	
	
	
	#and let's make those movement values
	moveX = (oPlayer['d'] - oPlayer['a'])
	moveY = (oPlayer['w'] - oPlayer['s'])
	
	#apply the movement values to the actuator and actuate
	aPlayerMotion.useLocalDLoc = True
	aPlayerMotion.dLoc = (moveX, moveY, 0)
	cont.activate(aPlayerMotion)

#function for jumping
#
#Things that need implementing:
#	-Double Jump
def jump(cont):
	#get Player object
	oPlayer = cont.owner
	
	#get the Character controller from oPlayer
	cPlayer = bge.constraints.getCharacter(oPlayer)
	
	#and get the keyboard
	kbd = bge.logic.keyboard
	
	#check if the jump key's been pressed
	if(kbd.events[bge.events.SPACEKEY] > 0):
		#if it has been, run the jump function to jump (duh)
		cPlayer.jump()
