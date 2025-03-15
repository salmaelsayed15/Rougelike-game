# Roguelike Adventure

A grid-based roguelike game built with Python and Pygame Zero featuring gem collection, and enemy avoidance.

## What's Needed to Run the Game?

### Libraries Used

- Python 3.6 or higher
- Pygame Zero (pgzrun)
- Pygame (automatically installed with Pygame Zero)
- Math (standard library)
- Random (standard library)

### Installation Steps

1. Install Python from [python.org](https://python.org)
2. Install Pygame Zero using pip:
   ```
   pip install pgzero
   ```
3. Run the game:
   ```
   python main.py
   ```

## Game Description

1. **Dungeon Exploration**: Navigate through a grid-based dungeon with walls and open spaces
2. **Collectible Gems**: Find and gather all gems scattered throughout the level
3. **Enemy Avoidance**: Avoid three types of enemies - ghosts, skeletons, and slimes
4. **Health System**: Manage your health points while facing enemies
5. **Animated Characters**: Enjoy smooth animations for the player character and enemies
6. **Sound Effects**: Experience audio feedback for game actions
7. **Background Music**: Listen to background music while playing

## Code Structure

- **main.py**: Main game loop, renders graphics, handles input, and manages game state
- **player.py**: Player class with movement controls, animation, and health system
- **enemy.py**: Base enemy class and specific enemy types (Ghost, Skeleton, Slime)
- **menu.py**: Menu interface with buttons for game options

## How to Play the Game?

### Controls

- **Arrow Keys** or **WASD**: Move the player character
- **ESC**: Return to the main menu
- **Mouse**: Click on menu buttons

### Interface

- Health hearts at the top-left of the screen
- Score and gem count at the top-right
- Menu with options for:
  - Start Game
  - Toggle Music (ON/OFF)
  - Toggle Sound (ON/OFF)
  - Exit

## Win and Lose Condition

### Win Condition

- Collect all gems in the level
- A "You Win!" screen appears with your final score
- Click to return to the main menu

### Lose Condition

- Lose all three health points by colliding with enemies
- A "Game Over" screen appears with your final score
- Click to return to the main menu

## Health System

- Player starts with 3 health points
- Each enemy collision removes 1 health point
- After being hit, the player becomes temporarily invulnerable (flashing effect)
- Health is displayed as hearts in the top-left corner
- When health reaches 0, the game ends

## Functions Used

### Main Game Functions

- **initialize_game()**: Sets up the game environment, player, enemies, and collectibles
- **update()**: Updates game objects and checks for collisions each frame
- **draw()**: Renders all game elements to the screen
- **is_valid_move()**: Validates player and enemy movement against walls and boundaries

### Sound Functions

- **play_sound()**: Plays specified sound effects with volume management
- **stop_sound()**: Stops a currently playing sound
- **toggle_music()** and **toggle_sound()**: Enable/disable game audio

### Player Functions

- **move_up()**, **move_down()**, **move_left()**, **move_right()**: Handle directional movement
- **take_damage()**: Reduces player health and triggers invulnerability
- **update()**: Handles player animation and movement

### Enemy Functions

- **change_direction()**: Randomly changes enemy movement direction
- **collides_with()**: Detects collision with the player
- **update()**: Updates enemy position and animation

## Game Mechanics

### Movement System

- Grid-based movement with smooth transitions between cells
- Collision detection prevents walking through walls
- One-cell-at-a-time movement for the player

### Enemy AI

- Random movement with direction changes
- Each enemy type has different movement speeds:
  - Ghost: Slow (1.5 speed) with erratic movement
  - Skeleton: Medium speed (2.0)
  - Slime: Slowest (1.0)
- Enemies bounce off walls and boundaries

### Collectible System

- Gems placed throughout the level
- 100 points per gem collected
- Visual and audio feedback when collecting gems

## Game Assets

### Sounds

- **game_over.wav**: [https://freesound.org/people/noirenex/sounds/159408/](https://freesound.org/people/noirenex/sounds/159408/)
- **gem_collect.wav**: [https://freesound.org/people/MLaudio/sounds/615099/](https://freesound.org/people/MLaudio/sounds/615099/)
- **hurt.wav**: [https://freesound.org/people/EminYILDIRIM/sounds/568795/](https://freesound.org/people/EminYILDIRIM/sounds/568795/)
- **win.wav**: [https://freesound.org/people/Fupicat/sounds/521645/](https://freesound.org/people/Fupicat/sounds/521645/)

### Sprites

All sprite sheets and individual sprite frames were custom created:

- Created original SVG graphics for each character
- Manipulated SVG files to create animation frames
- Extracted each frame as a PNG file for use in the game
- Organized in directories by character type and animation direction
