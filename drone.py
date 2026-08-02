from ursina import *
import random
from config import *

class Drone(Entity):
    def __init__(self, position=(0,5,0), color_value=color.azure):
        super().__init__()

        self.position = position
        self.speed = DRONE_SPEED
        self.target = self.random_target()

        self.model = Entity(
        parent=self,
        model='assets/drone_body.glb',
        scale=1
        )

        # Body
        # self.body = Entity(
        #     parent=self,
        #     model='cube',
        #     color=color_value,
        #     scale=(1.5,0.3,1)
        # )

        # # Arms
        # Entity(
        #     parent=self,
        #     model='cube',
        #     color=color.black,
        #     scale=(3,0.05,0.1)
        # )

        # Entity(
        #     parent=self,
        #     model='cube',
        #     color=color.black,
        #     scale=(0.1,0.05,3)
        # )

        # self.propellers=[]

        # prop_positions=[
        #     (1.4,0.15,1.4),
        #     (-1.4,0.15,1.4),
        #     (1.4,0.15,-1.4),
        #     (-1.4,0.15,-1.4)
        # ]

        # for p in prop_positions:
        #     prop=Entity(
        #         parent=self,
        #         model='cube',
        #         color=color.red,
        #         scale=(0.8,0.02,0.1),
        #         position=p
        #     )
        #     self.propellers.append(prop)

    def random_target(self):
        return Vec3(
            random.uniform(-WORLD_LIMIT,WORLD_LIMIT),
            random.uniform(MIN_HEIGHT,MAX_HEIGHT),
            random.uniform(-WORLD_LIMIT,WORLD_LIMIT)
        )

    def update_drone(self,drones):

        if distance(self.position,self.target)<1:
            self.target=self.random_target()

        direction=(self.target-self.position).normalized()

        avoid=Vec3(0,0,0)

        for d in drones:

            if d==self:
                continue

            dist=distance(self.position,d.position)

            if dist<SAFE_DISTANCE and dist>0:

                avoid+=(self.position-d.position).normalized()*(SAFE_DISTANCE-dist)

        direction+=avoid*2

        if direction.length()>0:
            direction=direction.normalized()

        self.position+=direction*self.speed*time.dt

        # Keep inside world

        self.x=max(-WORLD_LIMIT,min(WORLD_LIMIT,self.x))
        self.z=max(-WORLD_LIMIT,min(WORLD_LIMIT,self.z))
        self.y=max(MIN_HEIGHT,min(MAX_HEIGHT,self.y))

        # Rotate toward movement

        if direction.length()>0:
            self.look_at(self.position+Vec3(direction.x,0,direction.z))

        # Rotate propellers

        # for prop in self.propellers:
        #     prop.rotation_y += ROTATION_SPEED*time.dt