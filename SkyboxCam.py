import bge


def getSkyboxCam(cont):
	#get the skybox scene
	for scene in bge.logic.getSceneList():
		#if the scene is found, take the active camera from the skybox scene and return it
		if scene.name == cont.owner["skybox"]:
			return scene.active_camera
	#if the camera wasn't found, return None
	return None
	
def updateCameras(gameCam, skyboxCam):
	#copy the lens and projection matricies
	skyboxCam.lens = gameCam.lens
	skyboxCam.projection_matrix = gameCam.projection_matrix
	
	#copy the rotation of the cam to the skybox cam
	#be sure to use worldOrientation, because the cam doesn't rotate always rotate around it's local axis
	skyboxCam.worldOrientation = gameCam.worldOrientation

def update(cont):
	#we only want to do stuff if there's something filled in the "skybox" property
	if cont.owner["skybox"] not "":
		#get the skybox cam (if it exists)
		skyboxCam = getSkyboxCam(cont)
		if skyboxCam not None:
			#update the cameras!
			updateCameras(cont.owner, skyboxCam)
			