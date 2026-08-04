from enum import Enum
from typing import Any

class MissionEventType(Enum):
    MISSION_STARTED = "MissionStarted"
    MISSION_PAUSED = "MissionPaused"
    MISSION_RESUMED = "MissionResumed"
    WAYPOINT_REACHED = "WaypointReached"
    MISSION_COMPLETED = "MissionCompleted"
    MISSION_CANCELLED = "MissionCancelled"
    MISSION_FAILED = "MissionFailed"

class MissionEvent:
    def __init__(self, event_type: MissionEventType, mission_id: str, drone_id: str, data: Any = None):
        self.event_type = event_type
        self.mission_id = mission_id
        self.drone_id = drone_id
        self.data = data
