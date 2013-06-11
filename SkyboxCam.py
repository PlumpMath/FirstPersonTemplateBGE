import bge

class SkyboxCam:
	def __init__(self, cont):
		self.cont = cont
		
		#get the player camera
		self.oPlayer = self.cont.owner
		
		#get the PlayerCam object
		for obj in self.oPlayer.children:
			if type(obj) == bge.types.KX_Camera:
				self.oPlayerCam = obj
		
		#if there's a camera mentioned in the skyboxCam prop
		if self.oPlayer["skyboxCam"] != "":
			#get the camera we want to send the rotation changes to
			#
			#we loop through all active scenes in the engine
			for scene in bge.logic.getSceneList():
				#if the active camera in the scene has the correct name, it's our gameCam
				if scene.active_camera.name == self.oPlayer["skyboxCam"]:
					self.skyboxCam = scene.active_camera
			
							
	def update(self):
		#copy the lens and projection matricies
		self.skyboxCam.lens = self.oPlayerCam.lens
		self.skyboxCam.projection_matrix = self.oPlayerCam.projection_matrix
		
		#copy the rotation of the cam to the skybox cam
		#be sure to use worldOrientation, because the cam doesn't rotate always rotate around it's local axis
		self.skyboxCam.worldOrientation = self.oPlayerCam.worldOrientation

		
skybox_cam = SkyboxCam(bge.logic.getCurrentController())

def main():
	skybox_cam.update()