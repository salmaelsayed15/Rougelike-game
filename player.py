import math
from pygame.rect import Rect

class Player:
    def __init__(self, x, y, cell_size):
        # Position variables
        self.x = x  # Current x position
        self.y = y  # Current y position
        self.target_x = x  # Target x position for movement
        self.target_y = y  # Target y position for movement
        self.move_speed = 5  # Pixels per frame 
        self.cell_size = cell_size
        
        # Animation variables
        self.direction = "down"  # Current facing direction
        self.frame = 0  # Current animation frame
        self.animation_speed = 0.1  # Time between frame changes 
        self.animation_timer = 0  # Timer for animation
        self.is_moving = False  # Whether the player is currently moving
        self.frames_per_direction = 4  # Number of frames in each animation
        
        # Health system
        self.max_health = 3
        self.health = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.max_invulnerable_time = 60  # 1 second of invulnerability after being hit
        
        # Limit movement to one cell at a time
        self.movement_locked = False
    
    def update(self):
        # Update animation timer
        self.animation_timer += 1
        
        # Update invulnerability timer
        if self.invulnerable:
            self.invulnerable_timer += 1
            if self.invulnerable_timer >= self.max_invulnerable_time:
                self.invulnerable = False
                self.invulnerable_timer = 0
        
        # If we reach the target position, stop moving
        if self.is_moving and abs(self.x - self.target_x) < self.move_speed and abs(self.y - self.target_y) < self.move_speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False
        
        # If still moving, update position
        if self.is_moving:
            # Calculate direction vector
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            
            # Normalize direction vector
            distance = math.sqrt(dx * dx + dy * dy)
            if distance > 0:
                dx = dx / distance * self.move_speed
                dy = dy / distance * self.move_speed
            
            # Update position
            self.x += dx
            self.y += dy
        
        # Update animation frame - animate even when standing still, but at different rates
        if self.is_moving:
            # Animate faster when moving
            if self.animation_timer >= 30 * self.animation_speed:  # Lower threshold = faster animation
                self.frame = (self.frame + 1) % self.frames_per_direction
                self.animation_timer = 0
        else:
            # Animate slower when standing still
            if self.animation_timer >= 60 * self.animation_speed:
                self.frame = (self.frame + 1) % self.frames_per_direction
                self.animation_timer = 0
    
    def draw(self, screen):
        # Determine which sprite to use based on direction and frame
        sprite_name = f"player/player_{self.direction}_{self.frame}"
        
        # Draw the sprite at the current position with flashing effect if invulnerable
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            # Skip drawing to create flashing effect
            pass
        else:
            screen.blit(sprite_name, (self.x, self.y))
        
        # Draw health
        self.draw_health(screen)
    
    def draw_health(self, screen):
        # Draw health hearts at the top-left of the screen
        for i in range(self.max_health):
            heart_color = (220, 20, 60) if i < self.health else (100, 100, 100)  # Red for health, gray for empty
            heart_x = 20 + i * 30
            heart_y = 20
            
            # Draw a simple heart shape using circles
            screen.draw.filled_circle((heart_x, heart_y), 10, heart_color)
            screen.draw.filled_circle((heart_x + 10, heart_y), 10, heart_color)
            # Draw a filled rect for the bottom of the heart
            screen.draw.filled_rect(Rect(heart_x - 5, heart_y, 20, 10), heart_color)
    
    def take_damage(self):
        if not self.invulnerable:
            self.health -= 1
            self.invulnerable = True
            return True  # Damage was actually taken
        return False  # No damage taken (invulnerable)
    
    def is_dead(self):
        return self.health <= 0
    
    def move_up(self):
        if not self.is_moving:  # Only move if not already moving
            self.direction = "up"
            # Store current position
            old_target_y = self.target_y
            # Set new target
            self.target_y = self.y - self.cell_size
            self.is_moving = True
            # The actual validation of this move will happen in main.py's update function
    
    def move_down(self):
        if not self.is_moving:  # Only move if not already moving
            self.direction = "down"
            # Store current position
            old_target_y = self.target_y
            # Set new target
            self.target_y = self.y + self.cell_size
            self.is_moving = True
            # The actual validation of this move will happen in main.py's update function
    
    def move_left(self):
        if not self.is_moving:  # Only move if not already moving
            self.direction = "left"
            # Store current position
            old_target_x = self.target_x
            # Set new target
            self.target_x = self.x - self.cell_size
            self.is_moving = True
            # The actual validation of this move will happen in main.py's update function
    
    def move_right(self):
        if not self.is_moving:  # Only move if not already moving
            self.direction = "right"
            # Store current position
            old_target_x = self.target_x
            # Set new target
            self.target_x = self.x + self.cell_size
            self.is_moving = True
            # The actual validation of this move will happen in main.py's update function
    
    def cancel_movement(self):
        self.target_x = self.x
        self.target_y = self.y
        self.is_moving = False
    
    def get_rect(self):
        # Return a rectangle representing the player's hitbox
        return Rect(self.x + 10, self.y + 10, self.cell_size - 20, self.cell_size - 20)