from pygame.rect import Rect

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Define button positions and sizes
        button_width = 200
        button_height = 50
        button_margin = 20
        button_x = screen_width // 2 - button_width // 2
        button_y_start = screen_height // 2 - (3 * button_height + 2 * button_margin) // 2
        
        # Create button rectangles
        self.start_button = Rect(button_x, button_y_start, button_width, button_height)
        self.music_button = Rect(button_x, button_y_start + button_height + button_margin, button_width, button_height)
        self.sound_button = Rect(button_x, button_y_start + 2 * (button_height + button_margin), button_width, button_height)
        self.exit_button = Rect(button_x, button_y_start + 3 * (button_height + button_margin), button_width, button_height)
        
        # Music and sound states (initialized to True in main.py)
        self.music_on = True
        self.sound_on = True
        
    def update_button_states(self, music_on, sound_on):
        """Update the button states to reflect the current settings"""
        self.music_on = music_on
        self.sound_on = sound_on
    
    def draw(self, screen):
        # Draw title
        screen.draw.text("Roguelike Adventure", (self.screen_width // 2, 100), 
                         centerx=self.screen_width // 2, color="white", fontsize=60)
        
        # Draw buttons with different colors for on/off states
        self.draw_button(screen, self.start_button, "Start Game", (100, 100, 200))
        
        music_color = (100, 200, 100) if self.music_on else (200, 100, 100)
        music_text = "Music: ON" if self.music_on else "Music: OFF"
        self.draw_button(screen, self.music_button, music_text, music_color)
        
        sound_color = (100, 200, 100) if self.sound_on else (200, 100, 100)
        sound_text = "Sound: ON" if self.sound_on else "Sound: OFF"
        self.draw_button(screen, self.sound_button, sound_text, sound_color)
        
        self.draw_button(screen, self.exit_button, "Exit", (200, 100, 100))
    
    def draw_button(self, screen, rect, text, color):
        screen.draw.filled_rect(rect, color)
        screen.draw.rect(rect, (255, 255, 255))
        screen.draw.text(text, rect.center, centerx=rect.centerx, centery=rect.centery, color="white")
    
    def check_button_click(self, pos):
        # Check if any button was clicked
        if self.start_button.collidepoint(pos):
            return "start"
        elif self.music_button.collidepoint(pos):
            self.music_on = not self.music_on
            return "music"
        elif self.sound_button.collidepoint(pos):
            self.sound_on = not self.sound_on
            return "sound"
        elif self.exit_button.collidepoint(pos):
            return "exit"
        return None