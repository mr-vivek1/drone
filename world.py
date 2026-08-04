
import random
from ursina import *
from config import *


class World:

    def __init__(self, environment):
        self.environment = environment

        # Sky
        Sky()

        # Sun Light
        self.sun = DirectionalLight()
        self.sun.look_at(Vec3(1,-1,-1))

        AmbientLight(color=color.rgba(120,120,120,0.5))

        # Ground
        self.ground = Entity(
            model='plane',
            scale=(GROUND_SIZE,1,GROUND_SIZE),
            texture='white_cube',
            texture_scale=(GROUND_SIZE,GROUND_SIZE),
            color=color.rgb(50,180,50),
            collider='box'
        )

        self.create_from_environment()

    def create_from_environment(self):
        from navigation.obstacles import BoxObstacle
        for obs in self.environment.obstacles:
            if isinstance(obs, BoxObstacle):
                # Ursina cube is centered at 0,0,0 with scale 1. 
                # obs.size is total scale (width, height, depth)
                # obs.center is world position
                Entity(
                    model='cube',
                    position=obs.center,
                    scale=obs.half_size * 2,
                    color=color.gray if obs.half_size.x > 10 else color.light_gray
                )