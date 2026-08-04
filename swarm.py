from drone import Drone
from config import *
from sim.simulator import Simulator
from ursina import *


class Swarm:

    def __init__(self):
        # Initialize the core simulation
        self.simulator = Simulator(target_hz=60)
        self.drones = []
        self.selected_drone = None
        self.selection_callback = None
        
        self.colors = [
            color.azure, color.orange, color.red, color.yellow,
            color.cyan, color.magenta, color.green, color.lime,
            color.violet, color.white
        ]

        # Initialize with existing sim drones (if any)
        self._sync_visual_drones(self.simulator.swarm_model.drones)
        
    def _sync_visual_drones(self, sim_drones):
        for drone_model in sim_drones:
            self._create_visual_drone(drone_model)

    def _create_visual_drone(self, drone_model):
        color_val = self.colors[len(self.drones) % len(self.colors)]
        drone_entity = Drone(
            sim_model=drone_model,
            color_value=color_val
        )
        drone_entity.selection_callback = self._on_drone_clicked
        self.drones.append(drone_entity)
        return drone_entity

    def spawn_drones(self, count):
        new_sim_drones = self.simulator.swarm_model.spawn_drones(count)
        self._sync_visual_drones(new_sim_drones)

    def remove_drone(self, drone_entity):
        if drone_entity == self.selected_drone:
            self.select_drone(None)
            
        success = self.simulator.swarm_model.remove_drone(drone_entity.sim_model.id)
        if success:
            self.drones.remove(drone_entity)
            destroy(drone_entity)

    def _on_drone_clicked(self, drone_entity):
        self.select_drone(drone_entity)

    def select_drone(self, drone_entity):
        if self.selected_drone:
            self.selected_drone.is_selected = False
        
        self.selected_drone = drone_entity
        
        if self.selected_drone:
            self.selected_drone.is_selected = True
            
        if self.selection_callback:
            self.selection_callback(self.selected_drone)

    def update(self):
        # Advance the numeric simulation using the engine's delta time
        self.simulator.tick(time.dt)
        
        manager = self.simulator.swarm_model.mission_manager
        
        # Update visuals to match the new simulation state
        for drone in self.drones:
            active_wp = None
            if drone.sim_model.id in manager.active_assignments:
                active_wp = manager.active_assignments[drone.sim_model.id].mission.active_waypoint
                
            drone.sync_visuals(active_wp)

    def get_drones(self):
        return self.drones