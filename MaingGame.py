# MainGame.py - The primary game entry point

# 1. External Library Imports
from ursina import *
from ursina.shaders import basic_lighting_shader
from math import floor, sqrt
import random
# tkinter is only imported by the Menu classes, not here.

# 2. Relative Imports from the 'Game' folder
# These imports link the classes to the files we just created.
from Game.Car import Car
from Game.Police import PoliceCar
from Game.PolicePointer import PolicePointer
from Game.GameCam import GameCamera
from Game.Terrains import PhysicsTerrainManager, CityGenerator, TerrainManager
from Game.CustomShaders import CustomShaders

# 3. Relative Imports from the 'Menus' folder
from Menus.MainMenu import MainMenu
from Menus.Worldselector import WorldSelector
from Menus.Gameover import GameOverMenu

class MainGame(Entity):
    """
    Handles the game's core logic, state, and connections between all components.
    Subclasses Entity to use Ursina's update/input system.
    """
    def __init__(self):
        super().__init__()
        
        # Game State Variables (originally global)
        self.time_counter = 0.0
        self.police_enabled_timer = 0.0
        self.turn = 0.0 # Steering rotation
        self.pause = 1 # 1=playing, 0=paused
        self.police_speed = 3.5 # Initial default, updated by WorldSelector

        # Initialize core components (Ursina setup)
        random.seed(random.randint(0, 100))
        self.setup_ursina_environment()

        # Initialize Entities (Ursina is paused until a world is selected)
        self.car = Car()
        self.police = PoliceCar()
        self.pointer = PolicePointer(self.car)
        self.terrain_manager = TerrainManager(self.car)
        self.camera_handler = GameCamera(self.car, self.police)
        self.camera_handler.set_toggle_callback(self.toggle_pause_via_editor)

        # UI Text
        self.time_text = Text(
            text='Time: 0.00',
            position=window.top_left + Vec2(0.1, -0.05),
            origin=(0, 0),
            color=color.black,
            background=False,
            scale=1.25
        )
        self.time_text.color = color.orange

        # Start the game flow with the main menu (blocking Tkinter call)
        application.pause()
        self.show_main_menu()

    def setup_ursina_environment(self):
        """Sets up window properties and fixed scene elements."""
        window.color = color.white
        window.exit_button.visible = False
        window.fps_counter.enabled = True
        window.entity_counter.enabled = False
        window.collider_counter.enabled = False
        window.cog_button.enabled = False
        window.forced_aspect_ratio = 16/9
        window.borderless = False
        mouse.locked = False
        
        # Background elements
        scene.fog_color = color.white50
        scene.fog_density = 0.06
        Sky(texture='sky_sunset.jpg')
        # Audio
        Audio('carbgmusic.mp3', loop=True, autoplay=True)

    # --- Game State Management ---

    def show_main_menu(self):
        """Opens the main menu."""
        MainMenu(self.show_world_selector)

    def show_world_selector(self):
        """Opens the world selection menu."""
        WorldSelector(self.start_game)

    def show_game_over(self):
        """Opens the game over menu."""
        self.pause = 0
        application.pause()
        GameOverMenu(self.time_counter, self.restart_game, self.quit_game)

    def reset_game_state(self):
        """Resets all game logic variables."""
        self.time_counter = 0.0
        self.police_enabled_timer = 0.0
        self.turn = 0.0
        self.pause = 1
        application.resume()

    def start_game(self, world_type, police_speed):
        """Starts the game with selected settings."""
        self.police_speed = police_speed
        self.set_world_shader(world_type)
        self.reset_game_state()
        application.resume() # Unpause Ursina

    def restart_game(self):
        """Resets entities and state for a fresh game start."""
        self.reset_game_state()
        
        # Reset Entity Positions (using the initial values from the original file)
        self.car.position = Vec3(10, 30, 10)
        self.car.rotation = Vec3(0, 0, 0)
        self.car.model_visual.position = Vec3(10, 30, 10)
        self.car.model_visual.rotation = Vec3(0, 0, 0)

        self.police.position = Vec3(10, 30, -20)
        self.police.rotation = Vec3(0, 180, 0)
        
        # Reset Camera
        self.camera_handler.editor_camera.enabled = False
        camera.position = Vec3(0, 5, -10)
        camera.rotation = Vec3(30, 180, 0)
        
        # Return to world selector to ensure police speed/world choice is confirmed
        self.show_world_selector()

    def quit_game(self):
        """Exits the entire application."""
        self.reset_game_state()
        application.quit()

    def set_world_shader(self, world_type):
        """Applies the correct shader to the camera."""
        if world_type == 'normal':
            # FIX: Use the color grading shader for enhancement
            camera.shader = CustomShaders.color_grade_shader 
        elif world_type == 'retro':
            camera.shader = CustomShaders.pixelation_shader
        elif world_type == 'hybrid':
            camera.shader = CustomShaders.empty_shader

    def toggle_pause_via_editor(self, is_playing):
        """Callback to sync MainGame pause state when EditorCamera is toggled."""
        self.pause = 1 if is_playing else 0
        self.pointer.enabled = is_playing

    # --- Ursina Input and Update Logic ---

    def input(self, key):
        """Handles player steering input and game over call."""
        if self.pause == 0:
            return # Ignore input if paused by game over
        
        # Steering via Scroll (from original logic)
        if key == 'scroll up':
            self.turn -= 0.25
        elif key == 'scroll down':
            self.turn += 0.25
        
        self.turn = max(min(self.turn, 3), -3) # Clamp steering input

        # Escape key to show Game Over menu
        if key == 'escape':
            self.show_game_over()
            
    def update(self):
        """The main game loop logic, called every frame."""
        # 1. Update Game Timer
        if self.pause == 1:
            self.time_counter += time.dt
            self.police_enabled_timer += time.dt
        self.time_text.text = f'Time: {self.time_counter:.2f}'

        # 2. Player Movement and Rotation
        move = self.car.move_speed if self.car.y <= 0 else self.car.move_speed_air
        self.car.position += self.car.back * move * time.dt * self.pause

        # Player Rotation Input (A/D and Mouse)
        rotation_rate = 3
        if held_keys['left mouse'] or held_keys['a']:
            self.car.rotation_y -= rotation_rate
            self.turn = 0
        elif held_keys['right mouse'] or held_keys['d']:
            self.car.rotation_y += rotation_rate
            self.turn = 0
        else:
            self.car.rotation_y += self.turn * self.pause
        
        # 3. Terrain Raycast and Car Update
        hit_info = raycast(self.car.world_position + Vec3(0, 1000, 0), direction=Vec3(0, -1, 0), distance=2000, ignore=(self.car, self.terrain_manager.water, self.car.model_visual))
        
        ground_y = hit_info.world_point.y if hit_info.hit else None
        hit_info_normal = hit_info.normal if hit_info.hit else None
        
        self.car.update_visual(self.pause, ground_y, hit_info_normal)

        # 4. Police AI and Collision
        if self.police_enabled_timer > 15:
            # Police movement
            self.police.position += self.police.back * time.dt * self.police_speed * self.pause
            
            # Police look-at logic
            self.police.look_at(self.car.model_visual.position)
            self.police.rotation_y += 180 # Correction to make it face forward
            self.police.rotation_z = 0
            self.police.rotation_x = 0

            # Game Over check
            if distance(self.car.model_visual.position, self.police.position) <= 1:
                self.show_game_over()

        # Police ground snap (raycast)
        p_hit_info = raycast(self.police.world_position + Vec3(0, 1000, 0), direction=Vec3(0, -1, 0), distance=2000, ignore=(self.terrain_manager.water, self.car.model_visual, self.car))
        if p_hit_info.hit and p_hit_info.world_point.y is not None:
           # Police slowly lerp to ground height
           self.police.y = lerp(self.police.y, p_hit_info.world_point.y + 0.06, 7 * time.dt)


        # 5. Update Components
        self.terrain_manager.update()
        self.pointer.update_target(self.police.world_position)
        self.camera_handler.update(self.pause)


# --- Application Entry Point ---
if __name__ == '__main__':
    # Initialize Ursina app
    app = Ursina()
    
    # Initialize and run the MainGame instance
    game = MainGame()

    # The Ursina application is run after the Tkinter flow completes.
    app.run()