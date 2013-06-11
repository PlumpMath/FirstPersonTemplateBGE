import bge

class SkyboxCam:
	def __init__(self, cont):
		self.cont = cont
		
		#the owner is the camera, so let's get that
		self.gameCam = self.cont.owner
		
		#check to see if the skybox prop has anything in it
		#if it's empty main won't do much of anything
		if self.gameCam["skybox"] != "":
			self.hasSkybox = True
			#let's also create the background scene with an actuator
			self.aScene = self.cont.actuators["Scene"]
			self.aScene.scene = self.gameCam["skybox"]
			self.cont.activate(self.aScene)
		else:
			self.hasSkybox = False
		#we can't get the skybox camera during init because the background scene doesn't exist yet
		#instead we create a boolean indicating the camera hasn't yet been found
		self.gotSkyboxCam = False
		
		
		
	def getSkyboxCam(self):
		#create a skyboxCam variable and assign it null
		self.skyboxCam = None
		#get the skybox scene
		for scene in bge.logic.getSceneList():
			if scene.name == self.gameCam["skybox"]:
				self.skyboxCam = scene.active_camera
		#if the camera wasn't found, skyboxCam will still be None
		if self.skyboxCam is None:
			self.gotSkyboxCam = False
		else:
			self.gotSkyboxCam = True
		
	def update(self):
		#copy the lens and projection matricies
		self.skyboxCam.lens = self.gameCam.lens
		self.skyboxCam.projection_matrix = self.gameCam.projection_matrix
		
		#copy the rotation of the cam to the skybox cam
		#be sure to use worldOrientation, because the cam doesn't rotate always rotate around it's local axis
		self.skyboxCam.worldOrientation = self.gameCam.worldOrientation

		
skybox_cam = SkyboxCam(bge.logic.getCurrentController())

def main():
	#always check to see if the data has been freed, and if so re-init
	if skybox_cam.cont.invalid:
		skybox_cam.__init__(bge.logic.getCurrentController())
	
	#only run update if there's a skyboxCam
	if skybox_cam.hasSkybox:
		#next we get the skybox camera ONLY if we haven't already found it
		if not skybox_cam.gotSkyboxCam:
			skybox_cam.getSkyboxCam()
		else:
			skybox_cam.update()