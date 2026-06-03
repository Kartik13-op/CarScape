# CarScape

CarScape is a Python driving game built with the Ursina game engine and Tkinter menus. The player controls a car while avoiding a police car in an endless procedural world with selectable visual themes.

## Features

- Player-controlled car with rotation and procedural terrain interaction
- Police AI chase mechanic with game over condition
- Three world modes: Normal, Retro, and Hybrid Dark
- Tkinter menus for start, world selection, and game over screens
- Procedural terrain generation with water and city-style building generation
- Custom shaders for visual effects

## Repository Structure

- `MaingGame.py` - Main application entry point
- `Game/` - Game logic and entity classes
  - `Car.py`
  - `Police.py`
  - `PolicePointer.py`
  - `GameCam.py`
  - `Terrains.py`
  - `CustomShaders.py`
- `Menus/` - Tkinter menu screens
  - `MainMenu.py`
  - `Worldselector.py`
  - `Gameover.py`
- `Assets/` - 3D models, audio, and game assets
  - `BananaCar.glb`
  - `Car Hatchback.glb`
  - `Police Car.glb`
  - `carbgmusic.mp3`

## Prerequisites

- Python 3.10+ recommended
- `ursina` game engine
- `tkinter` (standard library on Windows)

## Installation

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv venv
.\
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Game

From the repository root:

```powershell
python MaingGame.py
```

## How to Play

- Survive as long as possible while being chased by the police car.
- Choose a world mode and police speed before starting.
- The police car begins chasing after a short delay.
- If the police car reaches you, the game ends and the Game Over menu appears.

## Controls

- `A` or `Right Mouse Button` - Turn right
- `D` or `Left Mouse Button` - Turn left
- Mouse scroll wheel - Adjust steering input. Hold mouse in both hands horizontally and use scroll wheel like a joystick to steer precisely.
- `Escape` - Trigger the Game Over screen
- `Tab` - Toggle the editor camera view (and pause state)

## Notes

- The game uses Tkinter for menu UI, so no additional GUI dependency is required on Windows.
- If you change the entrypoint filename, update the command above accordingly.

## License

This repository does not include a license file.
