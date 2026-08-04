import random
from config import *
from sim.drone_model import DroneModel
from sim.spatial_index import SpatialHashGrid
from sim.collision_avoidance import CollisionAvoidance
from time import perf_counter

from missions.mission_types import HoverMission, WaypointMission, PatrolMission, ReturnHomeMission, PlannedMission
from missions.mission_assignment import MissionAssignment
from missions.mission_manager import MissionManager
from missions.waypoint import Waypoint
from ursina import Vec3
from navigation.environment import Environment
from navigation.obstacles import SphereObstacle, BoxObstacle, CylinderObstacle

class SwarmModel:
    """Pure simulation model for the entire swarm.
    
    Holds the DroneModels and the SpatialHashGrid, decoupled from any rendering.
    """
    def __init__(self, num_drones=0):
        self.drones = []
        self.grid = SpatialHashGrid(cell_size=GRID_CELL_SIZE)
        self.collision_avoidance = CollisionAvoidance()
        self.mission_manager = MissionManager()
        self.environment = Environment()
        self._next_drone_id = 1
        
        # Add static obstacles for path planning demonstration
        self.environment.add_obstacle(SphereObstacle(Vec3(0, 10, 0), radius=3.0))
        self.environment.add_obstacle(BoxObstacle(Vec3(10, 10, 10), size=Vec3(4, 20, 4)))
        self.environment.add_obstacle(CylinderObstacle(Vec3(-10, 0, -10), radius=2.5, height=20.0))
        
        # Performance profiling 
        self._frame = 0
        self._sample_interval = 60
        self._last_naive_time = 0.0
        self._last_grid_time = 0.0

        if num_drones > 0:
            self.spawn_drones(num_drones)

    def spawn_drones(self, count):
        new_drones = []
        for _ in range(count):
            position = (
                random.uniform(-25, 25),
                random.uniform(5, 12),
                random.uniform(-25, 25)
            )
            readable_id = f"UAV-{self._next_drone_id:03d}"
            self._next_drone_id += 1
            
            drone_model = DroneModel(position=position, readable_id=readable_id)
            self.drones.append(drone_model)
            self.grid.insert(drone_model)
            new_drones.append(drone_model)
            
            # Note: No automatic mission assignment as per requirements. Start in Idle.
            
        return new_drones

    def remove_drone(self, drone_id):
        for d in self.drones:
            if d.id == drone_id:
                self.drones.remove(d)
                self.grid.remove(d)
                self.mission_manager.cancel_mission(d.id)
                return True
        return False

    def update(self, dt: float, physics_engine, environment=None):
        """Advances the swarm state by one tick."""
        self._frame += 1
        
        # Performance sampling: compare naive O(N^2) vs spatial grid
        if self._frame % self._sample_interval == 0:
            n = len(self.drones)
            
            # Naive
            t0 = perf_counter()
            for drone in self.drones:
                neighbors = []
                for d in self.drones:
                    if d is drone:
                        continue
                    if (drone.position - d.position).length() < SAFE_DISTANCE:
                        neighbors.append(d)
            t1 = perf_counter()
            self._last_naive_time = t1 - t0

            # Grid
            t0 = perf_counter()
            for drone in self.drones:
                neigh = self.grid.query_radius(drone.position, SAFE_DISTANCE)
            t1 = perf_counter()
            self._last_grid_time = t1 - t0

            if DEBUG_MODE:
                print(f"[spatial_index] N={n} naive={self._last_naive_time:.6f}s grid={self._last_grid_time:.6f}s")

        # Advance missions
        drone_states_dict = {drone.id: drone.position for drone in self.drones}
        active_waypoints = self.mission_manager.update(dt, drone_states_dict)

        # The new update pipeline
        for drone in self.drones:
            # Spatial query
            neighbors = self.grid.query_radius(drone.position, SAFE_DISTANCE)
            neighbor_positions = [d.position for d in neighbors if d is not drone]
            
            # 1. Update high-level logic (e.g. check waypoint reached)
            drone.update_logic()
            
            # 2. Flight Controller generates desired motion towards active waypoint
            active_waypoint = active_waypoints.get(drone.id)
            command = drone.controller.update(dt, active_waypoint=active_waypoint)
            
            # 3. Collision Avoidance modifies motion if necessary
            safe_command = self.collision_avoidance.process(command, drone.state, neighbor_positions)
            
            # 4. Physics Engine applies motion limits and kinematics
            physics_engine.step(drone.state, safe_command, dt, environment)
            
            # 5. Update grid membership after movement
            self.grid.update(drone)

    def get_drone(self, drone_id):
        for drone in self.drones:
            if drone.id == drone_id:
                return drone
        return None

    def assign_hover(self, drone_id):
        drone = self.get_drone(drone_id)
        if drone:
            mission = HoverMission(position=drone.position, altitude=drone.position.y)
            assignment = MissionAssignment(drone_id, mission)
            self.mission_manager.assign_mission(drone_id, assignment)
            self.mission_manager.start_mission(drone_id)

    def assign_waypoint(self, drone_id):
        drone = self.get_drone(drone_id)
        if drone:
            # Generate a random waypoint nearby for demonstration
            wp_pos = Vec3(drone.position.x + random.uniform(-15, 15), 
                          drone.position.y, 
                          drone.position.z + random.uniform(-15, 15))
            wp = Waypoint("rand_wp", position=wp_pos)
            mission = WaypointMission([wp])
            assignment = MissionAssignment(drone_id, mission)
            self.mission_manager.assign_mission(drone_id, assignment)
            self.mission_manager.start_mission(drone_id)

    def assign_patrol(self, drone_id):
        drone = self.get_drone(drone_id)
        if drone:
            import math
            # Generate a circular patrol path
            radius = 15.0
            center = drone.position
            waypoints = []
            num_points = 4
            for i in range(num_points):
                angle = (2 * math.pi / num_points) * i
                wx = center.x + radius * math.cos(angle)
                wz = center.z + radius * math.sin(angle)
                wp = Waypoint(f"patrol_{i}", position=Vec3(wx, center.y, wz))
                waypoints.append(wp)
                
            mission = PatrolMission(waypoints)
            assignment = MissionAssignment(drone_id, mission)
            self.mission_manager.assign_mission(drone_id, assignment)
            self.mission_manager.start_mission(drone_id)

    def assign_return_home(self, drone_id):
        drone = self.get_drone(drone_id)
        if drone:
            mission = ReturnHomeMission(home_position=drone.home_position, return_altitude=15.0)
            assignment = MissionAssignment(drone_id, mission)
            self.mission_manager.assign_mission(drone_id, assignment)
            self.mission_manager.start_mission(drone_id)
