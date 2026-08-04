from navigation.straight_line import StraightLinePlanner
from navigation.astar import AStarPlanner
from navigation.rrt import RRTPlanner
from navigation.rrt_star import RRTStarPlanner

class PlannerFactory:
    @staticmethod
    def create_planner(name: str):
        name = name.lower().strip()
        if name == "straight":
            return StraightLinePlanner()
        elif name == "a*":
            return AStarPlanner()
        elif name == "rrt":
            return RRTPlanner()
        elif name == "rrt*":
            return RRTStarPlanner()
        else:
            raise ValueError(f"Unknown planner name: {name}")
