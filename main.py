from ursina import *

from world import World
from swarm import Swarm
from camera_controller import DroneCamera
from ui_manager import UIManager

# Create Ursina App
app = Ursina()

# Window Settings
window.title = "Drone Swarm Simulator"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True
window.fps_counter.enabled = True

# Create Swarm
swarm = Swarm()

# Create World
world = World(swarm.simulator.environment)

# Create Camera
camera_controller = DroneCamera()

# Create Operator Console UI
ui_manager = UIManager(swarm, camera_controller)

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
        
    elif key == 'p':
        if swarm.simulator.is_paused:
            swarm.simulator.resume()
        else:
            swarm.simulator.pause()
            
    elif key == 'o':
        swarm.simulator.set_speed(0.5)
    elif key == 'i':
        swarm.simulator.set_speed(1.0)
    elif key == 'u':
        swarm.simulator.set_speed(2.0)
    elif key == 'y':
        swarm.simulator.set_speed(5.0)

# Update Loop
def update():
    swarm.update()
    ui_manager.update()

# Run Application
app.run()