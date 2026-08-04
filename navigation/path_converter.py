from missions.waypoint_queue import WaypointQueue
from missions.waypoint import Waypoint
from navigation.path import Path

class PathConverter:
    """Converts a Navigation Path into a Mission WaypointQueue."""
    
    @staticmethod
    def to_queue(path: Path, base_speed: float = 4.0, acceptance_radius: float = 1.0) -> WaypointQueue:
        queue = WaypointQueue()
        if not path or not path.waypoints:
            return queue
            
        for i, pos in enumerate(path.waypoints):
            wp = Waypoint(
                waypoint_id=f"wp_{path.planner_name}_{i}",
                position=pos,
                desired_speed=base_speed,
                acceptance_radius=acceptance_radius
            )
            queue.add_waypoint(wp)
            
        return queue
