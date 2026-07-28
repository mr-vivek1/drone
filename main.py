from ursina import *

from world import World
from swarm import Swarm
from camera_controller import DroneCamera

# Create Ursina App
app = Ursina()

# Window Settings
window.title = "Drone Swarm Simulator"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True
window.fps_counter.enabled = True

# Create World
world = World()

# Create Camera
camera_controller = DroneCamera()

# Create Swarm
swarm = Swarm()

# Information Panel
Text(
    text="""
Drone Swarm Simulator

Controls
-----------------------
Right Mouse  : Rotate
Middle Mouse : Pan
Scroll Wheel : Zoom

Press:
1 - Default View
2 - Top View
3 - Side View
4 - Front View
""",
    x=-0.87,
    y=0.43,
    background=True
)

# Keyboard Controls
def input(key):

    if key == '1':
        camera_controller.reset()

    elif key == '2':
        camera_controller.top_view()

    elif key == '3':
        camera_controller.side_view()

    elif key == '4':
        camera_controller.front_view()

# Update Loop
def update():
    swarm.update()

# Run Application
app.run()