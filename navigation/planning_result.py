from typing import Dict, Any
from navigation.path import Path

class PlanningResult:
    """Encapsulates the output and metrics of a planning request."""
    def __init__(self, path: Path, planner_name: str, success: bool = True):
        self.path = path
        self.planner_name = planner_name
        self.success = success
        self.planning_time = 0.0
        self.nodes_expanded = 0
        self.iterations = 0
        self.total_cost = path.total_length if path else 0.0
        self.metadata: Dict[str, Any] = {}

    def print_benchmark(self):
        from config import DEBUG_MODE
        if not DEBUG_MODE:
            return
            
        print(f"\n--- Benchmark: {self.planner_name} ---")
        print(f"Success:      {self.success}")
        print(f"Time:         {self.planning_time:.4f} s")
        print(f"Path Length:  {self.total_cost:.2f}")
        if self.path:
            print(f"Waypoints:    {len(self.path.waypoints)}")
        print(f"Expanded:     {self.nodes_expanded}")
        print(f"Iterations:   {self.iterations}")
        print("-----------------------------------")
