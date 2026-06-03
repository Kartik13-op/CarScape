from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina.prefabs.trail_renderer import TrailRenderer

class PoliceCar(Entity):
    """
    Represents the police car enemy.
    """
    def __init__(self, position=Vec3(10, 30, -20), rotation=Vec3(0, 180, 0), **kwargs):
        super().__init__(
            model='Police Car.glb',
            scale=(1, 1, 1),
            shader=basic_lighting_shader,
            position=position,
            rotation=rotation,
            origin=(0, 0, -0.5)
        )
        # ptr = TrailRenderer(...) # Trail renderer is commented out in original, so I'll keep it out.
