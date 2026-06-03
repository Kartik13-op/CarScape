from ursina import *
from ursina.shaders import basic_lighting_shader


class Car(Entity):
    """
    Represents the player-controlled car.
    It encapsulates both the collision entity (self) and the visual model (self.model_visual).
    """
    def __init__(self, position=Vec3(10, 30, 10), rotation=Vec3(0, 0, 0), **kwargs):
        # 1. Logic/Collision Entity (Invisible cube)
        super().__init__(
            model='cube',
            color=color.rgba(149, 149, 149, 0),
            scale=0.2,
            position=position,
            rotation=rotation,
            collider='box'
        )
        self.gravity_lerp_speed = 4 # From original logic
        self.move_speed = 10 # Base movement speed
        self.move_speed_air = 20 # Air movement speed

        # 2. Visual Model
        self.model_visual = Entity(
            model='Car Hatchback.glb',
            scale=(1, 1, 1),
            shader=basic_lighting_shader,
            origin=(0, 0, -0.5)
        )
        # tr = TrailRenderer(...) # Trail renderer is commented out in original, so I'll keep it out.

    def update_visual(self, pause_state, ground_y, hit_info_normal):
        # Apply ground collision physics and rotation
        if ground_y:
            # Gravity/Ground snap logic (from original update)
            if self.y > ground_y + 0.06:
                self.y = lerp(self.y, ground_y + 0.1, time.dt * self.gravity_lerp_speed)
            elif self.y < ground_y + 0.1:
                self.y = lerp(self.y, ground_y + 0.1, time.dt * 5 * self.gravity_lerp_speed)

        # Update visual model's position and rotation
        self.model_visual.position = lerp(self.model_visual.position, self.position, 4 * time.dt * pause_state)
        self.model_visual.rotation_y = self.rotation_y
