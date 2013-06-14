import bge
import mathutils
import math

#our initialization stuff
def init(cont):
	
	#get the PlayerCam object
	for obj in cont.owner.children:
		if type(obj) == bge.types.KX_Camera:
			cont.owner["playerCam"] = obj
	
	#the initial pitch of the camera
	cont.owner["camRotation"] = 90.0
	
	#center the mouse from the get-go so it doesn't skip around anywhere at all
	bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))

#the main method that does all the stuff
def update(cont):
	
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
	pitchLimit(cont)
	
	#make the rotation matrix and apply it to the camera
	cont.owner["playerCam"].localOrientation = mathutils.Matrix.Rotation(math.radians(cont.owner["camRotation"]), 3, 'X')
	
	#Actuate the actuators
	cont.activate(aPlayerMotion)

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
def pitchLimit(cont):
	#the camera has it's own rotation property, so let's add mousePosition[1] to that
	cont.owner["camRotation"] += mouseOffset[1] * -cont.owner["rotYspeed"]
	#next, make sure the rotation doesn't go outside the max and min defined in Player
	if cont.owner["camRotation"] > cont.owner["rotMax"]:
		cont.owner["camRotation"] = cont.owner["rotMax"]
	if cont.owner["camRotation"] < cont.owner["rotMin"]:
		cont.owner["camRotation"] = cont.owner["rotMin"]
		
