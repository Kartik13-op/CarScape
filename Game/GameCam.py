from ursina import *

class GameCamera:
    """
    Handles the camera positioning, follow logic, and jiggle effects.
    Uses Ursina's global 'camera' entity and 'editor_camera' for pause.
    """
    def __init__(self, car_instance, police_car_instance):
        self.car = car_instance
        self.police_car = police_car_instance

        # Camera positioning entities (from original code)
        self.camorigin = Entity(position=(0, 3, 6))
        self.camorigin.parent = self.car.model_visual
        
        # Initial camera settings
        camera.fov = 60
        camera.position = Vec3(0, 5, -10)
        camera.rotation = Vec3(30, 180, 0)

        # Pause Handler for EditorCamera (tab key)
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)
        self.pause_handler = Entity(ignore_paused=True, input=self.toggle_editor)
        self.toggle_callback = None # To be set by MainGame

    def set_toggle_callback(self, callback):
        self.toggle_callback = callback

    def toggle_editor(self, key):
        if key == 'tab':
            self.editor_camera.enabled = not self.editor_camera.enabled
            application.paused = self.editor_camera.enabled
            self.editor_camera.position = self.car.model_visual.position
            
            if self.toggle_callback:
                self.toggle_callback(not self.editor_camera.enabled)


    def update(self, pause_state):
        # 1. Camera Follow Logic (from original update)
        camera.position = lerp(camera.position, self.camorigin.world_position, 5 * time.dt)
        camera.y = 6 # fixed Y offset from the ground
        camera.look_at(self.car.model_visual)
        camera.rotation_z = 0 # Prevent tilt

        # 2. Camera Jiggle Logic (applied to cars as per original code)
        t = time.time() * 1.5
        jiggle_strength = 0.02
        scale_x = 1 + math.sin(t * 25) * jiggle_strength
        scale_y = 1 + math.cos(t * 30) * jiggle_strength * 2
        scale_z = 1 + math.sin(t * 20) * jiggle_strength * 0.5
        jiggle_scale = Vec3(scale_x, scale_y, scale_z)

        self.car.model_visual.scale = jiggle_scale
        self.police_car.scale = jiggle_scale
