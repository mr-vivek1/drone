from drone import Drone
from config import *

import random
from ursina import *


class Swarm:

    def __init__(self):

        self.drones = []

        colors = [
            color.azure,
            color.orange,
            color.red,
            color.yellow,
            color.cyan,
            color.magenta,
            color.green,
            color.lime,
            color.violet,
            color.white
        ]

        for i in range(NUMBER_OF_DRONES):

            drone = Drone(
                position=(
                    random.uniform(-25, 25),
                    random.uniform(5, 12),
                    random.uniform(-25, 25)
                ),
                color_value=colors[i % len(colors)]
            )

            self.drones.append(drone)

    def update(self):

        for drone in self.drones:
            drone.update_drone(self.drones)

    def get_drones(self):
        return self.drones