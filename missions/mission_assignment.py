from missions.mission import Mission, MissionStatus
import time

class MissionAssignment:
    """Links a Drone to a Mission with metadata."""
    def __init__(self, drone_id: str, mission: Mission, priority: int = 1, metadata=None):
        self.drone_id = drone_id
        self.mission = mission
        self.priority = priority
        self.metadata = metadata or {}
        self.start_time = None
        
    @property
    def status(self) -> MissionStatus:
        return self.mission.status
