import pgzrun
import math
from pygame import Rect

# Game constants
WIDTH = 800
HEIGHT = 600
TITLE = "Roguelike Adventure"

# Game states
MENU = 0
PLAYING = 1
game_state = MENU

# Sound settings
sound_on = True
music_on = True

# Grid settings
GRID_SIZE = 50
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Player
player = None

# Enemies
enemies = []

# Level data - 0: empty, 1: wall
level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Game objects
walls = []

# Menu buttons
start_button = Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
sound_button = Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
exit_button = Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

class Player:
    def __init__(self, x, y):
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.speed = 3
        self.direction = 'down'
        self.moving = False
        self.animation_timer = 0
        self.frame = 0
        self.frames = 4  # Number of animation frames

    def update(self):
        # Move towards target position
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        if abs(dx) > 0.1 or abs(dy) > 0.1:
            self.moving = True
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'

            # Move towards target
            if abs(dx) > 0.1:
                self.x += math.copysign(min(self.speed, abs(dx)), dx)
            if abs(dy) > 0.1:
                self.y += math.copysign(min(self.speed, abs(dy)), dy)
        else:
            self.moving = False
            self.x = self.target_x
            self.y = self.target_y

        # Update animation
        self.animation_timer += 1
        if self.animation_timer > 8:  # Animation speed
            self.animation_timer = 0
            self.frame = (self.frame + 1) % self.frames

    def move(self, dx, dy):
        new_grid_x = int((self.target_x + dx * GRID_SIZE) / GRID_SIZE)
        new_grid_y = int((self.target_y + dy * GRID_SIZE) / GRID_SIZE)

        # Check if the new position is valid (not a wall)
        if 0 <= new_grid_x < GRID_WIDTH and 0 <= new_grid_y < GRID_HEIGHT:
            if level[new_grid_y][new_grid_x] == 0:  # Not a wall
                self.target_x = new_grid_x * GRID_SIZE
                self.target_y = new_grid_y * GRID_SIZE
                if sound_on:
                    sounds.footstep.play()

    def draw(self):
        # Determine which sprite to use based on direction and animation frame
        sprite_name = f"player_{self.direction}_{self.frame}"
         # Comment this line out or fix it:
        # screen.blit(sprite_name, (self.x, self.y))
    
        # Instead, use this (uncomment it):
        screen.blit(f"player/player_{self.direction}_{self.frame}", (self.x, self.y))

        # Draw a colored rectangle instead of a sprite
        # screen.draw.filled_rect(Rect(self.x, self.y, GRID_SIZE, GRID_SIZE), (0, 255, 0))  # Green rectangle for player

class Enemy:
    def __init__(self, x, y, patrol_points, enemy_type):
        self.x = x * GRID_SIZE
        self.y = y * GRID_SIZE
        self.target_x = self.x
        self.target_y = self.y
        self.patrol_points = patrol_points
        self.current_point = 0
        self.speed = 2
        self.direction = 'down'
        self.moving = True
        self.animation_timer = 0
        self.frame = 0
        self.frames = 4  # Number of animation frames
        self.enemy_type = enemy_type

    def update(self):
        # Move towards current patrol point
        target = self.patrol_points[self.current_point]
        self.target_x = target[0] * GRID_SIZE
        self.target_y = target[1] * GRID_SIZE

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        if abs(dx) > 0.1 or abs(dy) > 0.1:
            self.moving = True
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'

            # Move towards target
            if abs(dx) > 0.1:
                self.x += math.copysign(min(self.speed, abs(dx)), dx)
            if abs(dy) > 0.1:
                self.y += math.copysign(min(self.speed, abs(dy)), dy)
        else:
            # Reached target, move to next patrol point
            self.current_point = (self.current_point + 1) % len(self.patrol_points)

        # Update animation
        self.animation_timer += 1
        if self.animation_timer > 10:  # Animation speed
            self.animation_timer = 0
            self.frame = (self.frame + 1) % self.frames

    

    def draw(self):
        if self.enemy_type == "slime":
            #slime
            screen.blit(f"enemies/slime/slime_{self.direction}_{self.frame}", (self.x, self.y))
        elif self.enemy_type == "ghost":
            #ghost
            screen.blit(f"enemies/ghost/ghost_{self.direction}_{self.frame}", (self.x, self.y))
        else:  #skeleton
            screen.blit(f"enemies/skeleton/skeleton_{self.direction}_{self.frame}", (self.x, self.y))

    def collides_with(self, player):
        # Check if enemy collides with player
        player_rect = Rect(player.x, player.y, GRID_SIZE, GRID_SIZE)
        enemy_rect = Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        return player_rect.colliderect(enemy_rect)

def initialize_game():
    global player, enemies, walls

    # Create player
    player = Player(1, 1)

    # Create enemies with patrol routes
    enemies = [
        Enemy(3, 2, [(3, 2), (3, 7), (7, 7), (7, 2)], "slime"),
        Enemy(12, 3, [(12, 3), (12, 9), (14, 9), (14, 3)], "ghost"),
        Enemy(5, 10, [(5, 10), (10, 10), (10, 8), (5, 8)], "skeleton")
    ]

    # Create wall objects
    walls = []
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[y][x] == 1:
                walls.append(Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Start music if enabled
    if music_on:
        music.play('background')
        music.set_volume(0.5)

def draw():
    screen.fill((0, 0, 0))

    if game_state == MENU:
        # Draw menu
        screen.fill((50, 50, 70))
        screen.draw.text("ROGUELIKE ADVENTURE", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white", shadow=(1, 1))

        # Draw buttons
        screen.draw.filled_rect(start_button, (100, 100, 200))
        screen.draw.text("Start Game", center=start_button.center, fontsize=30, color="white")

        screen.draw.filled_rect(sound_button, (100, 100, 200))
        sound_text = "Sound: ON" if sound_on else "Sound: OFF"
        screen.draw.text(sound_text, center=sound_button.center, fontsize=30, color="white")

        screen.draw.filled_rect(exit_button, (100, 100, 200))
        screen.draw.text("Exit", center=exit_button.center, fontsize=30, color="white")

    elif game_state == PLAYING:
        # Draw walls
        for wall in walls:
            screen.draw.filled_rect(wall, (100, 100, 100))

        # Draw player
        player.draw()

        # Draw enemies
        for enemy in enemies:
            enemy.draw()

def update():
    global game_state, sound_on, music_on

    if game_state == PLAYING:
        # Update player
        player.update()

        # Update enemies
        for enemy in enemies:
            enemy.update()

            # Check for collisions with enemies
            if enemy.collides_with(player):
                if sound_on:
                    sounds.hurt.play()
                # Reset player position
                player.x = 1 * GRID_SIZE
                player.y = 1 * GRID_SIZE
                player.target_x = player.x
                player.target_y = player.y

def on_key_down(key):
    global game_state
    if game_state == PLAYING:
        # Player movement
        if key == keys.UP:
            player.move(0, -1)
        elif key == keys.DOWN:
            player.move(0, 1)
        elif key == keys.LEFT:
            player.move(-1, 0)
        elif key == keys.RIGHT:
            player.move(1, 0)
        elif key == keys.ESCAPE:
            # Return to menu

            game_state = MENU

def on_mouse_down(pos, button):
    global game_state, sound_on, music_on

    if game_state == MENU:
        if start_button.collidepoint(pos):
            # Start the game
            game_state = PLAYING
            initialize_game()
            if sound_on:
                sounds.select.play()

        elif sound_button.collidepoint(pos):
            # Toggle sound
            sound_on = not sound_on
            music_on = sound_on

            if music_on:
                music.play('background')
                music.set_volume(0.5)
            else:
                music.stop()

        elif exit_button.collidepoint(pos):
            # Exit the game
            exit()

pgzrun.go()