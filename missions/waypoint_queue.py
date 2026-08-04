from collections import deque
from missions.waypoint import Waypoint

class WaypointQueue:
    """Manages a sequence of Waypoints."""
    def __init__(self):
        self.queue = deque()

    def add_waypoint(self, waypoint: Waypoint):
        self.queue.append(waypoint)

    def insert_waypoint(self, index: int, waypoint: Waypoint):
        self.queue.insert(index, waypoint)

    def remove_waypoint(self, waypoint_id: str):
        self.queue = deque(wp for wp in self.queue if wp.id != waypoint_id)

    def clear(self):
        self.queue.clear()

    def peek_next(self) -> Waypoint:
        if self.queue:
            return self.queue[0]
        return None

    def advance(self) -> Waypoint:
        """Pops and returns the current waypoint, advancing the queue."""
        if self.queue:
            return self.queue.popleft()
        return None

    def is_finished(self) -> bool:
        return len(self.queue) == 0
