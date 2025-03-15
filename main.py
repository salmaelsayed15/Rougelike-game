import pgzrun
import math
import random
from pygame.rect import Rect

from player import Player
from enemy import Enemy, Ghost, Skeleton, Slime
from menu import Menu

# Constants
WIDTH = 800
HEIGHT = 600
TITLE = "Roguelike Adventure"

# Cell size for grid-based movement
CELL_SIZE = 50

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
WIN = 3

# Initialize game state
game_state = MENU
previous_game_state = MENU  # Track previous state for sound changes
music_on = True
sound_on = True

# Sound state tracking
win_sound_playing = False
game_over_sound_playing = False

# Volume settings
NORMAL_MUSIC_VOLUME = 1.0  # Normal background music volume
LOWERED_MUSIC_VOLUME = 0.3  # Music volume when playing sound effects

# Flag to track if we're using custom gem sprites
use_custom_gems = True
gem_actors = []  # Store gem actors

# Original map - used as a template to reset the game
# 0 = empty space, 1 = wall, 2 = collectible
ORIGINAL_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Current map - this will change during gameplay
game_map = []

# Calculate map dimensions 
MAP_WIDTH = len(ORIGINAL_MAP[0])
MAP_HEIGHT = len(ORIGINAL_MAP)

# Collectibles
collectibles = []
total_collectibles = 0
collected = 0

# Score
score = 0

# Initialize game objects
player = None
enemies = []
menu = None

def reset_map():
    """Reset the game map to its original state"""
    global game_map
    game_map = []
    for row in ORIGINAL_MAP:
        game_map.append(row.copy())

def initialize_game():
    global player, enemies, menu, collectibles, total_collectibles, collected, score, game_over_sound_playing, win_sound_playing, gem_actors, use_custom_gems
    
    # Reset map to original state
    reset_map()
    
    # Reset collectibles and score
    collectibles = []
    gem_actors = []
    total_collectibles = 0
    collected = 0
    score = 0
    
    # Reset sound state
    game_over_sound_playing = False
    win_sound_playing = False
    
    # Create menu
    menu = Menu(WIDTH, HEIGHT)
    
    # Create player at starting position
    player = Player(2 * CELL_SIZE, 2 * CELL_SIZE, CELL_SIZE)
    
    # Create enemies
    enemies = [
        Ghost(5 * CELL_SIZE, 5 * CELL_SIZE, CELL_SIZE),
        Skeleton(10 * CELL_SIZE, 3 * CELL_SIZE, CELL_SIZE),
        Slime(8 * CELL_SIZE, 8 * CELL_SIZE, CELL_SIZE)
    ]
    
    # Set movement boundaries for enemies
    for enemy in enemies:
        # Only allow enemies to move within the playable area
        enemy.set_boundaries(1 * CELL_SIZE, (len(game_map[0])-2) * CELL_SIZE, 
                             1 * CELL_SIZE, (len(game_map)-2) * CELL_SIZE)
    
    # Find and initialize collectibles
    for y, row in enumerate(game_map):
        for x, cell in enumerate(row):
            if cell == 2:  # Collectible
                coll_x = x * CELL_SIZE
                coll_y = y * CELL_SIZE
                collectibles.append((coll_x, coll_y))
                
                # Create gem actors if we're using custom gems
                if use_custom_gems:
                    try:
                        # Create an Actor for each gem
                        # This will use gem.png from the images folder
                        new_gem = Actor('gem')
                        
                        # Set position
                        new_gem.pos = (coll_x + CELL_SIZE // 2, coll_y + CELL_SIZE // 2)
                        
                        # Scale the image to be smaller
                        # These values control the displayed size of the gem
                        # Adjust these to make the gems smaller or larger
                        new_gem.scale = 0.3  # Reduce size to 30% of original
                        
                        gem_actors.append(new_gem)
                    except:
                        # If there's an error, add None to keep the indexes aligned
                        gem_actors.append(None)
                        
                total_collectibles += 1
    
    # Check if we should use custom gems
    try:
        # Try creating a test actor to see if the gem image is available
        test_gem = Actor('gem')
        use_custom_gems = True
        print("Successfully loaded gem image")
    except Exception as e:
        print(f"Could not load gem image: {e}")
        use_custom_gems = False
    
    # Play background music if enabled and in the right game state
    play_background_music()

def play_background_music():
    """Play background music if enabled and in the right game state"""
    if music_on and (game_state == MENU or game_state == PLAYING):
        try:
            music.play('background')
            music.set_volume(NORMAL_MUSIC_VOLUME)
        except Exception as e:
            print(f"Error playing music: {e}")

def stop_background_music():
    """Stop background music"""
    try:
        music.stop()
    except Exception as e:
        print(f"Error stopping music: {e}")

def lower_music_volume():
    """Temporarily lower music volume to make sound effects more audible"""
    if music_on:
        try:
            music.set_volume(LOWERED_MUSIC_VOLUME)
        except Exception as e:
            print(f"Error lowering music volume: {e}")

def restore_music_volume():
    """Restore music volume to normal after playing sound effects"""
    if music_on:
        try:
            music.set_volume(NORMAL_MUSIC_VOLUME)
        except Exception as e:
            print(f"Error restoring music volume: {e}")

def schedule_restore_volume():
    """Schedule restoring the music volume after a short delay"""
    clock.schedule(restore_music_volume, 1.5)  # one and half second delay

def is_valid_move(x, y):
    # First, check window boundaries directly
    if not (0 <= x < WIDTH - CELL_SIZE and 0 <= y < HEIGHT - CELL_SIZE):
        return False
        
    # Then, convert pixel coordinates to grid coordinates
    grid_x = int(x / CELL_SIZE)
    grid_y = int(y / CELL_SIZE)
    
    # Finally check if position is within map bounds and not a wall
    if (0 <= grid_x < len(game_map[0]) and 
        0 <= grid_y < len(game_map) and 
        game_map[grid_y][grid_x] != 1):  # Allow collectibles (2) or empty space (0)
        return True
    return False

def toggle_music():
    global music_on, menu
    music_on = not music_on
    
    # Update menu button state
    if menu:
        menu.update_button_states(music_on, sound_on)
    
    if music_on and (game_state == MENU or game_state == PLAYING):
        play_background_music()
    else:
        stop_background_music()

def toggle_sound():
    global sound_on, menu
    sound_on = not sound_on
    
    # Update menu button state
    if menu:
        menu.update_button_states(music_on, sound_on)

def play_sound(sound_file):
    """Play a sound by its file name"""
    if not sound_on:
        return
    
    try:
        # First lower the music volume to make the sound effect more audible
        if game_state == PLAYING and music_on and (sound_file == "gem_collect" or sound_file == "hurt"):
            lower_music_volume()
            
        # Play the sound if it exists
        if hasattr(sounds, sound_file):
            sound = getattr(sounds, sound_file)
            
            # Use loops for important sounds
            if sound_file == "gem_collect":
                sound.play()
                clock.schedule(lambda: sound.play(), 0.1)  # Play twice for emphasis
            else:
                sound.play()
                
            # Schedule restoring the music volume
            if game_state == PLAYING and music_on and (sound_file == "gem_collect" or sound_file == "hurt"):
                schedule_restore_volume()
        else:
            print(f"Sound '{sound_file}' not found")
    except Exception as e:
        print(f"Error playing sound {sound_file}: {e}")

def stop_sound(sound_file):
    """Stop a currently playing sound"""
    try:
        if hasattr(sounds, sound_file):
            getattr(sounds, sound_file).stop()
    except Exception as e:
        print(f"Error stopping sound {sound_file}: {e}")

def draw_gem(screen, x, y):
    """Draw a gem using the original code method (fallback)"""
    # Draw a simple gem using filled_rect
    gem_color = (50, 200, 200)  # Teal color
    
    # Draw a diamond shape using rectangles
    screen.draw.filled_rect(Rect(x - 5, y - 5, 10, 10), gem_color)
    
    # Draw a shine
    screen.draw.filled_circle((x + 2, y - 2), 2, (255, 255, 255))

def draw():
    screen.clear()
    
    if game_state == MENU:
        menu.draw(screen)
    elif game_state == PLAYING:
        # Fill background with black (important for contrast)
        screen.fill((0, 0, 0))
        
        # Draw map (simple version)
        for y, row in enumerate(game_map):
            for x, cell in enumerate(row):
                if cell == 1:  # Wall
                    screen.draw.filled_rect(Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), (100, 100, 100))
                
                # Debug grid (optional - helpful for seeing boundaries)
                # screen.draw.rect(Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), (50, 50, 50))
        
        # Draw collectibles
        if use_custom_gems and gem_actors:
            # Draw collectibles using gem actors
            for i, (x, y) in enumerate(collectibles):
                if i < len(gem_actors) and gem_actors[i] is not None:
                    try:
                        gem_actors[i].draw()
                    except Exception as e:
                        print(f"Error drawing gem actor: {e}")
                        draw_gem(screen, x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                else:
                    # Fallback if something is wrong with the actor
                    draw_gem(screen, x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        else:
            # Draw collectibles using the original method
            for x, y in collectibles:
                draw_gem(screen, x + CELL_SIZE // 2, y + CELL_SIZE // 2)
        
        # Add boundary visualization at bottom of screen if needed
        for x in range(WIDTH // CELL_SIZE):
            if y * CELL_SIZE >= HEIGHT - CELL_SIZE:
                screen.draw.filled_rect(Rect(x * CELL_SIZE, HEIGHT - CELL_SIZE, CELL_SIZE, CELL_SIZE), (100, 100, 100))
        
        # Draw player
        player.draw(screen)
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)
        
        # Draw UI
        draw_ui(screen)
        
    elif game_state == GAME_OVER:
        screen.draw.text("Game Over", (WIDTH // 2, HEIGHT // 2 - 50), centerx=WIDTH // 2, color="white", fontsize=60)
        screen.draw.text(f"Score: {score}", (WIDTH // 2, HEIGHT // 2), centerx=WIDTH // 2, color="white", fontsize=40)
        screen.draw.text("Click to return to menu", (WIDTH // 2, HEIGHT // 2 + 50), centerx=WIDTH // 2, color="white", fontsize=30)
    
    elif game_state == WIN:
        screen.draw.text("You Win!", (WIDTH // 2, HEIGHT // 2 - 50), centerx=WIDTH // 2, color="white", fontsize=60)
        screen.draw.text(f"Score: {score}", (WIDTH // 2, HEIGHT // 2), centerx=WIDTH // 2, color="white", fontsize=40)
        screen.draw.text("Click to return to menu", (WIDTH // 2, HEIGHT // 2 + 50), centerx=WIDTH // 2, color="white", fontsize=30)

def draw_ui(screen):
    # Draw score
    score_text = f"Score: {score}"
    screen.draw.text(score_text, (WIDTH - 20, 20), right=WIDTH - 20, color="white", fontsize=30)
    
    # Draw collected items
    collect_text = f"Gems: {collected}/{total_collectibles}"
    screen.draw.text(collect_text, (WIDTH - 20, 50), right=WIDTH - 20, color="white", fontsize=30)

def update():
    global game_state, previous_game_state, player, enemies, collectibles, collected, score, game_over_sound_playing, win_sound_playing, gem_actors
    
    # Check for game state transitions
    if game_state != previous_game_state:
        if game_state == GAME_OVER and not game_over_sound_playing:
            # Stop background music and play game over sound
            stop_background_music()
            play_sound("game_over")
            game_over_sound_playing = True
        elif game_state == WIN and not win_sound_playing:
            # Stop background music and play win sound
            stop_background_music()
            play_sound("win")
            win_sound_playing = True
        elif (previous_game_state == GAME_OVER or previous_game_state == WIN) and (game_state == MENU or game_state == PLAYING):
            # Returning to menu or game from game over/win - resume background music
            play_background_music()
        
        previous_game_state = game_state
    
    if game_state == PLAYING:
        # First check if the player's target position is valid before updating
        if player.is_moving and not is_valid_move(player.target_x, player.target_y):
            player.cancel_movement()
        
        # Now update player with validated movement
        player.update()
        
        # Check for collectible collection
        player_rect = player.get_rect()
        for i, (x, y) in enumerate(collectibles[:]):
            collectible_rect = Rect(x + 10, y + 10, CELL_SIZE - 20, CELL_SIZE - 20)
            if player_rect.colliderect(collectible_rect):
                score += 100  # Add points directly to the global score (100 per gem)
                collectibles.pop(i)
                
                # Also remove the corresponding gem actor
                if i < len(gem_actors):
                    gem_actors.pop(i)
                    
                collected += 1
                play_sound("gem_collect")  # Play gem collection sound
                
                # Update map to remove the collected gem
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                game_map[grid_y][grid_x] = 0
                break
        
        # Update enemies
        for enemy in enemies:
            # First check if the enemy's target position is valid
            if enemy.is_moving and not is_valid_move(enemy.target_x, enemy.target_y):
                enemy.change_direction()
                
            # Now update enemy with validated movement
            enemy.update()
            
            # Check for collision between player and enemy
            if enemy.collides_with(player):
                if player.take_damage():  # Only play sound if damage was actually taken
                    play_sound("hurt")
                
                # Check if player is dead
                if player.is_dead():
                    game_state = GAME_OVER
        
        # Check win condition
        if collected >= total_collectibles:
            game_state = WIN

def on_mouse_down(pos):
    global game_state, game_over_sound_playing, win_sound_playing
    
    if game_state == MENU:
        button_clicked = menu.check_button_click(pos)
        
        if button_clicked == "start":
            game_state = PLAYING
            play_sound("select")
        elif button_clicked == "music":
            toggle_music()
            play_sound("select")
        elif button_clicked == "sound":
            toggle_sound()
            play_sound("select")
        elif button_clicked == "exit":
            exit()
    
    elif game_state == GAME_OVER:
        # Stop the game over sound
        stop_sound("game_over")
        game_over_sound_playing = False
        game_state = MENU
        initialize_game()
    
    elif game_state == WIN:
        # Stop the win sound
        stop_sound("win")
        win_sound_playing = False
        game_state = MENU
        initialize_game()

def on_key_down(key):
    global game_state
    if game_state == PLAYING:
        # Only process movement if player isn't already moving
        if not player.is_moving:
            if key == keys.UP or key == keys.W:
                player.move_up()
            elif key == keys.DOWN or key == keys.S:
                player.move_down()
            elif key == keys.LEFT or key == keys.A:
                player.move_left()
            elif key == keys.RIGHT or key == keys.D:
                player.move_right()
        
        if key == keys.ESCAPE:
            game_state = MENU
            play_sound("select")

# Initialize game on startup
initialize_game()

# Start the game
pgzrun.go()