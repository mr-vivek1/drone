from ursina import *
import random
from config import *
from sim.drone_model import DroneModel


class Drone(Entity):
    def __init__(self, sim_model, color_value=color.azure):
        super().__init__()
        self.collider = 'box'
        self.is_selected = False

        # Link to the pure numeric state
        self.sim_model = sim_model

        # Keep the entity positioned according to model
        self.position = self.sim_model.position

        self.speed = DRONE_SPEED

        # Body
        self.body = Entity(
            parent=self,
            model='cube',
            color=color_value,
            scale=(1.5, 0.3, 1)
        )

        # Arms
        Entity(
            parent=self,
            model='cube',
            color=color.black,
            scale=(3, 0.05, 0.1)
        )

        Entity(
            parent=self,
            model='cube',
            color=color.black,
            scale=(0.1, 0.05, 3)
        )

        self.propellers = []

        prop_positions = [
            (1.4, 0.15, 1.4),
            (-1.4, 0.15, 1.4),
            (1.4, 0.15, -1.4),
            (-1.4, 0.15, -1.4)
        ]

        for p in prop_positions:
            prop = Entity(
                parent=self,
                model='cube',
                color=color.red,
                scale=(0.8, 0.02, 0.1),
                position=p
            )
            self.propellers.append(prop)
            
        # Visual debugging: Waypoint marker
        self.waypoint_marker = Entity(
            model='sphere',
            color=color_value,
            scale=0.5,
            unlit=True,
            visible=False
        )
        
        # Readable ID Label
        self.id_label = Text(
            parent=self,
            text=self.sim_model.readable_id,
            y=2,
            scale=5,
            billboard=True,
            origin=(0,0)
        )
        
        # Selection Highlight (Ring)
        self.selection_ring = Entity(
            parent=self,
            model='circle',
            color=color.green,
            scale=(4, 4, 4),
            rotation_x=90,
            y=-0.5,
            unlit=True,
            visible=False
        )

    def on_click(self):
        # We will dispatch to a global selection manager in swarm.py or ui_manager
        if hasattr(self, 'selection_callback'):
            self.selection_callback(self)

    def sync_visuals(self, active_waypoint=None):
        """Update visuals to match the simulation model's current state."""
        # Sync visual entity to model state
        self.position = self.sim_model.position

        # Rotate toward movement (yaw only)
        if self.sim_model.heading.length() > 0:
            self.look_at(self.position + Vec3(self.sim_model.heading.x, 0, self.sim_model.heading.z))
            
        # Apply pitch and roll computed by the aerodynamics engine
        self.rotation_x = self.sim_model.state.pitch
        self.rotation_z = self.sim_model.state.roll

        # Rotate propellers for visual effect (uses rendering dt, not sim dt)
        for prop in self.propellers:
            prop.rotation_y += ROTATION_SPEED * time.dt
            
        # Update waypoint marker
        if active_waypoint:
            self.waypoint_marker.position = active_waypoint.position
            self.waypoint_marker.visible = True
        else:
            self.waypoint_marker.visible = False
            
        # Update selection highlight
        self.selection_ring.visible = self.is_selected