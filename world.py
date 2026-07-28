
import random
from ursina import *
from config import *


class World:

    def __init__(self):

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

        # Boundary markers
        self.create_boundaries()

        # Simple buildings
        self.create_buildings()

    def create_boundaries(self):

        thickness = 1
        height = 8
        size = WORLD_LIMIT * 2

        Entity(
            model='cube',
            scale=(size,height,thickness),
            position=(0,height/2,-WORLD_LIMIT),
            color=color.gray
        )

        Entity(
            model='cube',
            scale=(size,height,thickness),
            position=(0,height/2,WORLD_LIMIT),
            color=color.gray
        )

        Entity(
            model='cube',
            scale=(thickness,height,size),
            position=(-WORLD_LIMIT,height/2,0),
            color=color.gray
        )

        Entity(
            model='cube',
            scale=(thickness,height,size),
            position=(WORLD_LIMIT,height/2,0),
            color=color.gray
        )

    def create_buildings(self):

        positions = [
            (-20,0,-15),
            (15,0,-10),
            (-10,0,18),
            (18,0,20),
            (0,0,0)
        ]

        for x,y,z in positions:

            h = random.randint(4,10)

            Entity(
                model='cube',
                position=(x,h/2,z),
                scale=(4,h,4),
                color=color.light_gray
            )