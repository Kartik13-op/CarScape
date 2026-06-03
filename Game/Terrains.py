from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina.prefabs.trail_renderer import TrailRenderer

from ursina.scripts.property_generator import generate_properties_for_class
from ursina.entity import Entity
from ursina import scene, time
from ursina.vec3 import Vec3
from ursina.shaders import lit_with_shadows_shader, basic_lighting_shader, matcap_shader
import random
import math




class TerrainManager:
    """
    Manages the infinite, procedural mesh terrain generation and destruction.
    This class is almost identical to the original, just properly integrated.
    """
    def __init__(self, follow_target, tile_size=20, tile_resolution=20, render_range=1, terrain_height=3):
        self.follow_target = follow_target # The car entity
        self.tile_size = tile_size
        self.tile_resolution = tile_resolution
        self.render_range = render_range
        self.terrain_height = terrain_height
        self.generated_tiles = {}
        self.noise_grid = {} # Stores pre-calculated noise values for consistency

        # Water entity setup (from original code)
        self.water = Entity(model='plane', color=color.rgba(0, 125, 255, 0.5), scale=(100, 100, 100))

    def lerp(self, a, b, t):
        return a + t * (b - a)

    def smoothstep(self, t):
        return t * t * (3 - 2 * t)

    def value_noise(self, x, z):
        from math import floor
        x0, z0 = floor(x), floor(z)
        x1, z1 = x0 + 1, z0 + 1
        sx, sz = self.smoothstep(x - x0), self.smoothstep(z - z0)

        # Use noise_grid for consistency
        v00 = self.noise_grid.get((x0, z0), random.uniform(-1, 1))
        v10 = self.noise_grid.get((x1, z0), random.uniform(-1, 1))
        v01 = self.noise_grid.get((x0, z1), random.uniform(-1, 1))
        v11 = self.noise_grid.get((x1, z1), random.uniform(-1, 1))

        self.noise_grid[(x0, z0)] = v00
        self.noise_grid[(x1, z0)] = v10
        self.noise_grid[(x0, z1)] = v01
        self.noise_grid[(x1, z1)] = v11

        i1 = self.lerp(v00, v10, sx)
        i2 = self.lerp(v01, v11, sx)
        return self.lerp(i1, i2, sz)

    def generate_tile(self, tx, tz):
        key = (tx, tz)
        if key in self.generated_tiles:
            return

        mesh = Mesh()
        verts, tris, uvs, colors = [], [], [], []

        for z in range(self.tile_resolution):
            for x in range(self.tile_resolution):
                wx = tx * self.tile_size + (x / (self.tile_resolution - 1)) * self.tile_size
                wz = tz * self.tile_size + (z / (self.tile_resolution - 1)) * self.tile_size
                h = self.value_noise(wx / 8.0, wz / 8.0) * self.terrain_height
                verts.append(Vec3(wx, h, wz))
                uvs.append((x / self.tile_resolution, z / self.tile_resolution))

        for z in range(self.tile_resolution - 1):
            for x in range(self.tile_resolution - 1):
                i = x + z * self.tile_resolution
                tris += [(i, i + 1, i + self.tile_resolution), (i + 1, i + self.tile_resolution + 1, i + self.tile_resolution)]

        mesh.vertices = verts
        mesh.triangles = tris
        mesh.uvs = uvs
        mesh.colors = colors
        mesh.generate()

        tile_entity = Entity(model=mesh, collider='mesh', texture='grass.png')
        self.generated_tiles[key] = tile_entity

    def update(self):
        # Update terrain tiles
        px = int(self.follow_target.x // self.tile_size)
        pz = int(self.follow_target.z // self.tile_size)

        needed = set()
        for dx in range(-self.render_range, self.render_range + 1):
            for dz in range(-self.render_range, self.render_range + 1):
                key = (px + dx, pz + dz)
                needed.add(key)
                self.generate_tile(*key)

        for key in list(self.generated_tiles.keys()):
            if key not in needed:
                destroy(self.generated_tiles[key])
                del self.generated_tiles[key]
        
        # Update water position
        self.water.z = self.follow_target.model_visual.z
        self.water.x = self.follow_target.model_visual.x
        self.water.rotation_y = camera.rotation_y + 45 # Water rotation logic from original


class PhysicsTerrainManager:
    """
    Manages the infinite, procedural mesh terrain generation and destruction.
    This class is almost identical to the original, just properly integrated.
    """
    def __init__(self, follow_target, tile_size=10, tile_resolution=20, render_range=1, terrain_height=2):
        self.follow_target = follow_target # The car entity
        self.tile_size = tile_size
        self.tile_resolution = tile_resolution
        self.render_range = render_range
        self.terrain_height = terrain_height
        self.generated_tiles = {}
        self.noise_grid = {} # Stores pre-calculated noise values for consistency

        # Water entity setup (from original code)
        self.water = Entity(model='plane', color=color.rgba(0, 125, 255, 0.5), scale=(100, 100, 100))
        self.water.color = color.clear

    def lerp(self, a, b, t):
        return a + t * (b - a)

    def smoothstep(self, t):
        return t * t * (3 - 2 * t)

    def value_noise(self, x, z):
        from math import floor
        x0, z0 = floor(x), floor(z)
        x1, z1 = x0 + 1, z0 + 1
        sx, sz = self.smoothstep(x - x0), self.smoothstep(z - z0)

        # Use noise_grid for consistency
        v00 = self.noise_grid.get((x0, z0), random.uniform(-1, 1))
        v10 = self.noise_grid.get((x1, z0), random.uniform(-1, 1))
        v01 = self.noise_grid.get((x0, z1), random.uniform(-1, 1))
        v11 = self.noise_grid.get((x1, z1), random.uniform(-1, 1))

        self.noise_grid[(x0, z0)] = v00
        self.noise_grid[(x1, z0)] = v10
        self.noise_grid[(x0, z1)] = v01
        self.noise_grid[(x1, z1)] = v11

        i1 = self.lerp(v00, v10, sx)
        i2 = self.lerp(v01, v11, sx)
        return self.lerp(i1, i2, sz)

    def generate_tile(self, tx, tz):
        key = (tx, tz)
        if key in self.generated_tiles:
            return

        mesh = Mesh()
        verts, tris, uvs, colors = [], [], [], []

        for z in range(self.tile_resolution):
            for x in range(self.tile_resolution):
                wx = tx * self.tile_size + (x / (self.tile_resolution - 1)) * self.tile_size
                wz = tz * self.tile_size + (z / (self.tile_resolution - 1)) * self.tile_size
                h = self.value_noise(wx / 8.0, wz / 8.0) * self.terrain_height
                verts.append(Vec3(wx, h, wz))
                uvs.append((x / self.tile_resolution, z / self.tile_resolution))

        for z in range(self.tile_resolution - 1):
            for x in range(self.tile_resolution - 1):
                i = x + z * self.tile_resolution
                tris += [(i, i + 1, i + self.tile_resolution), (i + 1, i + self.tile_resolution + 1, i + self.tile_resolution)]

        mesh.vertices = verts
        mesh.triangles = tris
        mesh.uvs = uvs
        mesh.colors = colors
        mesh.generate()

        tile_entity = Entity(model=mesh, collider='mesh', texture='white_cube.png', shader=lit_with_shadows_shader, color=color.green)
        self.generated_tiles[key] = tile_entity

    def update(self):
        # Update terrain tiles
        px = int(self.follow_target.x // self.tile_size)
        pz = int(self.follow_target.z // self.tile_size)

        needed = set()
        for dx in range(-self.render_range, self.render_range + 1):
            for dz in range(-self.render_range, self.render_range + 1):
                key = (px + dx, pz + dz)
                needed.add(key)
                self.generate_tile(*key)

        for key in list(self.generated_tiles.keys()):
            if key not in needed:
                destroy(self.generated_tiles[key])
                del self.generated_tiles[key]

        
        # Update water position
        self.water.z = self.follow_target.z
        self.water.x = self.follow_target.x
        self.water.rotation_y = camera.rotation_y + 45 # Water rotation logic from original


class CityGenerator(Entity):
    def __init__(self, target, density=0.3, render_distance=80, grid_step=10, **kwargs):
        super().__init__(**kwargs)
        self.target = target              # The object to generate around (usually the player)
        self.density = density            # Probability (0.0 to 1.0) of a building spawning in a slot
        self.render_distance = render_distance 
        self.grid_step = grid_step        # Space between building centers
        self.cam = camera

        self.buildings = {}               # Dictionary to store {(x, z): entity}
        self.building_color_palette = [
            color.gray, color.light_gray, color.dark_gray, color.rgb(50, 50, 60), color.rgb(60, 70, 80), color.azure, color.cyan, color.rgb(200, 200, 220), color.rgb(180, 180, 200), color.rgb(220, 220, 240)
        ]

    def update(self):
        # 1. Determine where the player is on the "Grid"
        px = int(self.target.x / self.grid_step)
        pz = int(self.target.z / self.grid_step)

        # Calculate grid radius based on render distance
        grid_range = int(self.render_distance / self.grid_step)

        # 2. CLEANUP: Delete buildings that are too far away
        # We convert keys to a list to avoid "dictionary changed size during iteration" error
        for key in list(self.buildings.keys()):
            building = self.buildings[key]
            # Calculate simple 2D distance
            dist = distance_2d((building.x, building.z), (self.target.x, self.target.z))
            if dist > self.render_distance + self.grid_step:
                destroy(building)
                del self.buildings[key]

        # 3. GENERATION: Fill in the gaps around the player
        # We loop through a square grid around the player
        for x in range(px - grid_range, px + grid_range):
            for z in range(pz - grid_range, pz + grid_range):
                
                # Key for the dictionary
                key = (x, z)

                # Check if we already have a building here or if we already decided not to put one
                if key in self.buildings:
                    continue

                # Distance check for circle generation (makes it look less square)
                world_x = x * self.grid_step
                world_z = z * self.grid_step
                if distance_2d((world_x, world_z), (self.target.x, self.target.z)) > self.render_distance:
                    continue

                # DECISION: Should we spawn here?
                # We use a seed based on position so the world is "stable" 
                # (if you walk back, the same building is there, provided it wasn't deleted)
                random.seed(f"{x}_{z}") 
                
                if random.random() < self.density:
                    self.spawn_building(key, world_x, world_z)
                else:
                    # Mark as "empty" so we don't try to generate here again every frame
                    # We store None to indicate an empty processed slot
                    self.buildings[key] = Entity(visible=False) 

    def spawn_building(self, key, x, z):
        # Randomized dimensions
        w = random.uniform(4, 8)
        d = random.uniform(4, 8)
        h = random.uniform(5, 30) # Height variation

        b = Entity(
            model='cube',
            position=(x, (h/2)-3, z), # y is h/2 so the bottom sits on ground
            scale=(w, h, d),
            texture='white_cube',
            color=random.choice(self.building_color_palette),
            shader=basic_lighting_shader
        )
        
        # Add simple window-like texture variation (optional visual flair)
        b.texture_scale = (1, h/2) 

        self.buildings[key] = b
