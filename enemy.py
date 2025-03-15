import random
import math
from pygame.rect import Rect

class Enemy:
    def __init__(self, x, y, cell_size, enemy_type="ghost"):
        # Position variables
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.move_speed = 2  # Slower than player
        self.cell_size = cell_size
        self.enemy_type = enemy_type
        
        # Movement boundaries
        self.min_x = 0
        self.max_x = 800
        self.min_y = 0
        self.max_y = 600
        
        # Direction and movement
        self.directions = ["up", "down", "left", "right"]
        self.direction = random.choice(self.directions)
        self.is_moving = False
        self.movement_cooldown = 0
        
        # Animation variables
        self.frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.frames_per_direction = 4
    
    def set_boundaries(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
    
    def update(self):
        # Update animation timer
        self.animation_timer += 1
        
        # If we reach the target position, stop moving and set cooldown
        if self.is_moving and abs(self.x - self.target_x) < self.move_speed and abs(self.y - self.target_y) < self.move_speed:
            self.x = self.target_x
            self.y = self.target_y
            self.is_moving = False
            self.movement_cooldown = random.randint(30, 90)  # Wait 0.5-1.5 seconds
        
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
        else:
            # Decrement cooldown timer
            if self.movement_cooldown > 0:
                self.movement_cooldown -= 1
            else:
                # Choose a random direction and move
                self.change_direction()
        
        # Update animation frame
        if self.animation_timer >= 60 * self.animation_speed:
            self.frame = (self.frame + 1) % self.frames_per_direction
            self.animation_timer = 0
    
    def draw(self, screen):
        # Determine which sprite to use based on type, direction, and frame
        # Account for nested directory structure
        sprite_name = f"enemies/{self.enemy_type}/{self.enemy_type}_{self.direction}_{self.frame}"
        
        # Draw the sprite at the current position
        screen.blit(sprite_name, (self.x, self.y))
    
    def change_direction(self):
        self.direction = random.choice(self.directions)
        
        if self.direction == "up" and self.y - self.cell_size >= self.min_y:
            self.target_y = self.y - self.cell_size
            self.is_moving = True
        elif self.direction == "down" and self.y + self.cell_size <= self.max_y:
            self.target_y = self.y + self.cell_size
            self.is_moving = True
        elif self.direction == "left" and self.x - self.cell_size >= self.min_x:
            self.target_x = self.x - self.cell_size
            self.is_moving = True
        elif self.direction == "right" and self.x + self.cell_size <= self.max_x:
            self.target_x = self.x + self.cell_size
            self.is_moving = True
        else:
            # If movement would be out of bounds, try another direction
            self.change_direction()
    
    def get_rect(self):
        # Return a rectangle representing the enemy's hitbox
        return Rect(self.x + 10, self.y + 10, self.cell_size - 20, self.cell_size - 20)
    
    def collides_with(self, player):
        # Check if enemy collides with player
        return self.get_rect().colliderect(player.get_rect())


class Ghost(Enemy):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, "ghost")
        self.move_speed = 1.5  # Ghosts move slower
        self.animation_speed = 0.12


class Skeleton(Enemy):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, "skeleton")
        self.move_speed = 2.0  # Average speed
        self.animation_speed = 0.1


class Slime(Enemy):
    def __init__(self, x, y, cell_size):
        super().__init__(x, y, cell_size, "slime")
        self.move_speed = 1.0  # Slimes are the slowest
        self.animation_speed = 0.08