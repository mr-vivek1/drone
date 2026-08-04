# ==========================
# Drone Swarm Configuration
# ==========================

NUMBER_OF_DRONES = 10

GROUND_SIZE = 100

WORLD_LIMIT = 40

MIN_HEIGHT = 3
MAX_HEIGHT = 15

DRONE_SPEED = 4
ROTATION_SPEED = 2000

# Physics & Aerodynamics
GRAVITY = 9.81
DRONE_MASS = 1.0
MAX_THRUST = 20.0
DRAG_COEFFICIENT = 0.5

SAFE_DISTANCE = 3

CAMERA_DISTANCE = 60
CAMERA_HEIGHT = 35
# Spatial hash grid cell size (used by sim.spatial_index)
# Increase to cover more area per cell; tuning parameter for performance.
GRID_CELL_SIZE = 6

# ==========================
# Debug Configuration
# ==========================
DEBUG_MODE = False