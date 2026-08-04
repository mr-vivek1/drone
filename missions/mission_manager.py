from typing import Dict, List
import time
from missions.mission_assignment import MissionAssignment
from missions.mission_events import MissionEvent
from missions.mission import MissionStatus

class MissionManager:
    """Global orchestrator of all missions."""
    def __init__(self):
        # drone_id -> MissionAssignment
        self.active_assignments: Dict[str, MissionAssignment] = {}
        self.event_log: List[MissionEvent] = []

    def _handle_mission_event(self, event: MissionEvent):
        self.event_log.append(event)
        # Lightweight logging for debugging
        # print(f"[MissionEvent] {event.event_type.value} - Drone: {event.drone_id} - Mission: {event.mission_id}")

    def assign_mission(self, drone_id: str, assignment: MissionAssignment):
        """Assigns a mission to a drone. Overwrites any existing mission."""
        if drone_id in self.active_assignments:
            self.cancel_mission(drone_id)
            
        assignment.mission.initialize(drone_id, on_event_callback=self._handle_mission_event)
        self.active_assignments[drone_id] = assignment

    def start_mission(self, drone_id: str):
        if drone_id in self.active_assignments:
            assignment = self.active_assignments[drone_id]
            assignment.start_time = time.time()
            assignment.mission.start()

    def pause_mission(self, drone_id: str):
        if drone_id in self.active_assignments:
            self.active_assignments[drone_id].mission.pause()

    def resume_mission(self, drone_id: str):
        if drone_id in self.active_assignments:
            self.active_assignments[drone_id].mission.resume()

    def cancel_mission(self, drone_id: str):
        if drone_id in self.active_assignments:
            self.active_assignments[drone_id].mission.cancel()
            del self.active_assignments[drone_id]

    def update(self, dt: float, drone_states: dict) -> dict:
        """
        Steps all active missions.
        Takes a dict of {drone_id: drone_position}
        Returns a dict of {drone_id: active_waypoint}
        """
        active_waypoints = {}
        
        # Iterate over a list of keys to allow deletion during iteration
        for drone_id in list(self.active_assignments.keys()):
            assignment = self.active_assignments[drone_id]
            
            if drone_id not in drone_states:
                continue
                
            pos = drone_states[drone_id]
            waypoint = assignment.mission.update(dt, pos)
            
            if assignment.mission.status in [MissionStatus.COMPLETED, MissionStatus.CANCELLED, MissionStatus.FAILED]:
                # Mission is done, remove assignment
                del self.active_assignments[drone_id]
            else:
                active_waypoints[drone_id] = waypoint
                
        return active_waypoints
