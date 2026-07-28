from ursina import *
from ursina.prefabs.editor_camera import EditorCamera
from config import *


class DroneCamera:

    def __init__(self):

        self.camera = EditorCamera(
            enabled=True,
            rotation_speed=100,
            panning_speed=50,
            zoom_speed=2
        )

        self.reset()

    def reset(self):
        self.camera.position = (
            0,
            CAMERA_HEIGHT,
            -CAMERA_DISTANCE
        )

        self.camera.rotation = (30, 0, 0)

    def top_view(self):
        self.camera.position = (
            0,
            80,
            0
        )

        self.camera.rotation = (90, 0, 0)

    def side_view(self):
        self.camera.position = (
            CAMERA_DISTANCE,
            20,
            0
        )

        self.camera.rotation = (15, -90, 0)

    def front_view(self):
        self.camera.position = (
            0,
            20,
            -CAMERA_DISTANCE
        )

        self.camera.rotation = (15, 0, 0)

    def get_camera(self):
        return self.camera