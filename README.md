First Person Template
=====================

What is this?
-------------
The First Person Template is a first person template object for use with the Blender Game Engine. It's made up of a few different parts
*	The .blend contains two important objects, Player and PlayerCam. These two objects can be linked to any other blender file you might be working on and then made "local" so you can adjust all their properties
*	FPcontrols.py contains all the code needed for moving the player around and using mouselook
*	SkyboxCam.py controls the optional skybox you can set up for a scene

How do I use it?
----------------
Just link Player and PlayerCam from FPcontrols.blend to your project, make them both local so you can edit the various properties of the Player, and have at it!

Any standard controls?
----------------------
Yup! Keys are mapped as such:
*	W/A/S/D - Move around
*	Mouse - Look
*	Space - Jump
*	Shift - Sprint (or walk slowly; it triggers a speed multiplier)

Everything in this is free for use in whatever you like, just show me what you use it in so I can check it out! I'm always looking for new fun stuff to try out.
