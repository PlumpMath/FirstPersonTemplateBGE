import bge
import mathutils
import math
import inspect

class MouseLook:
	
	#our initialization stuff
	def __init__(self, cont):
		#get the controller
		self.cont = cont
		
		#get the Player object
		self.oPlayer = cont.owner
		
		#get the PlayerCam object
		for obj in self.oPlayer.children:
			if type(obj) == bge.types.KX_Camera:
				self.oPlayerCam = obj
		
		#get the PlayerMotion and CamMotion actuators
		self.aPlayerMotion = cont.actuators["PlayerMotion"]
		self.aCamMotion = cont.actuators["CamMotion"]
		
		#get the mouse
		self.mouse = bge.logic.mouse
		
		#get any custom properties
		self.deadzoneX = self.oPlayer["deadzoneX"]
		self.deadzoneY = self.oPlayer["deadzoneY"]
		self.rotXspeed = self.oPlayer["rotXspeed"]
		self.rotYspeed = self.oPlayer["rotYspeed"]
		self.rotMin = self.oPlayer["rotMin"]
		self.rotMax = self.oPlayer["rotMax"]
		
		#the initial pitch of the camera
		self.camRotation = 90.0
		
		#center the mouse from the get-go so it doesn't skip around anywhere at all
		bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))

	#this returns the change in mouse position
	def getMouseOffset(self):
		#Get the normalized mouse position
		#
		#This takes the mouse.position values, multiplies them by 2 and subtracts 1
		#so you get a value between -1 and 1 on the X and Y axis
		mousePosition = (self.mouse.position[0] * 2 - 1, self.mouse.position[1] * 2 - 1)
		
		#check the deadzones
		#if mouse.position falls within a deadzone value, mousePosition gets 0.0 assigned to that axis
		if(abs(mousePosition[0]) < self.deadzoneX):
			mx = 0.0
		else:
			mx = mousePosition[0] * self.rotXspeed
		if(abs(mousePosition[1]) < self.deadzoneY):
			my = 0.0
		else:
			my = mousePosition[1] * self.rotYspeed
		mousePosition = (mx, my)
		
		#center the mouse to the screen/window
		#
		#If we don't center the mouse to the screen rotation mayhem will occur
		bge.render.setMousePosition(int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))
		
		#return the mousePosition
		return mousePosition
		
	
	#the main method that does all the stuff
	def update(self):
		
		
		#get the mouse offset
		mouseOffset = self.getMouseOffset()
		
		#First we make sure we're using local rotation
		self.aPlayerMotion.useLocalDRot = True
		
		#Next, apply the x value of the mouse to the Z rotation of Player
		self.aPlayerMotion.dRot = [0, 0, -mouseOffset[0]]
		
		#PlayerCam rotation uses some freaky scary matrix stuff
		#This allows for precise control of the min and max rotation on the camera's local X axis
		#
		#the camera has it's own rotation property, so let's add mousePosition[1] to that
		self.camRotation += mouseOffset[1] * -self.rotYspeed
		#next, make sure the rotation doesn't go outside the max and min defined in Player
		if self.camRotation > self.rotMax:
			self.camRotation = self.rotMax
		if self.camRotation < self.rotMin:
			self.camRotation = self.rotMin
		
		#make the rotation matrix and apply it to the camera
		self.oPlayerCam.localOrientation = mathutils.Matrix.Rotation(math.radians(self.camRotation), 3, 'X')
		
		#Actuate the actuators
		self.cont.activate(self.aPlayerMotion)


mouse_look = MouseLook(bge.logic.getCurrentController())

def main():
	#always check to see if the data has been freed, and if so re-init
	if mouse_look.cont.invalid:
		mouse_look.__init__(bge.logic.getCurrentController())
	
	mouse_look.update()