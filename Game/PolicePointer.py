from ursina import *
from ursina.shaders import basic_lighting_shader


class PolicePointer(Entity):
    """
    An entity that points from the car to the police car, acting as a UI element.
    """
    def __init__(self, car_instance, **kwargs):
        super().__init__(
            model='cube',
            scale=(0.1, 0.1, 0.3),
            y=1,
            z=1,
            color=color.orange,
            origin=(0, 0, -1)
        )
        self.car = car_instance

    def update_target(self, police_position):
        # Position slightly above the car
        self.position = self.car.model_visual.position + Vec3(0, 0.4, 0)
        # Look at the police car
        self.look_at(police_position)
