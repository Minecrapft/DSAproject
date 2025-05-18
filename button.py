import pygame
from colors import Colors

#buttons class
class Image_Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #mouse position
        pos = pygame.mouse.get_pos()
        
        #mouse hover and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button on the screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class rect_Button:
    
    def __init__(self, x, y, width, height, text, font_size, font_color, color, hover_color, top_left, top_right, bottom_left, bottom_right):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.color = color
        self.hover_color = hover_color
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
        self.font = pygame.font.Font(None, font_size)
        
        # State tracking variables
        self.clicked = False
        self.is_hovering = False  # Track if the mouse is currently hovering
        self.hover_sound_played = False  # Track if hover sound has been played
        self.is_pressed = False  # Track if button is being pressed
        self.press_sound_played = False  # Track if press sound has been played
        
        # Load sounds only once during initialization
        try:
            self.hover_sound = pygame.mixer.Sound('clicksound.MP3')
        except:
            print("Warning: clicksound.MP3 not found")
            self.hover_sound = None
            
        try:
            self.press_sound = pygame.mixer.Sound('clicksound2.MP3')  # You can use different sounds
        except:
            print("Warning: clicksound.MP3 not found")
            self.press_sound = None

    def draw(self, surface):
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0] == 1
        
        # Check if mouse is over button
        hover_now = self.rect.collidepoint(mouse_pos)
        
        # Handle mouse states
        if hover_now:
            # Mouse is over button
            if mouse_pressed:
                # Button is being pressed
                if not self.is_pressed and self.press_sound and not self.press_sound_played:
                    # Play sound only on initial press
                    self.press_sound.play()
                    self.press_sound_played = True
                self.is_pressed = True
            else:
                # Mouse is over but not pressed
                if self.is_pressed:
                    # Just released the button
                    self.is_pressed = False
                    self.press_sound_played = False
                
                # Handle hover sound when not pressed
                if not self.is_hovering and self.hover_sound and not self.hover_sound_played:
                    self.hover_sound.play()
                    self.hover_sound_played = True
            
            self.is_hovering = True
            
            # Set visual state (pressed or hover)
            pygame.draw.rect(surface, self.hover_color, self.rect, 
                            border_top_left_radius=self.top_left, 
                            border_top_right_radius=self.top_right, 
                            border_bottom_left_radius=self.bottom_left, 
                            border_bottom_right_radius=self.bottom_right)
        else:
            # Mouse is not over button
            pygame.draw.rect(surface, self.color, self.rect, 
                        border_top_left_radius=self.top_left, 
                        border_top_right_radius=self.top_right, 
                        border_bottom_left_radius=self.bottom_left, 
                        border_bottom_right_radius=self.bottom_right)
            
            # Reset all states when mouse leaves
            if self.is_hovering:
                self.is_hovering = False
                self.hover_sound_played = False
            
            self.is_pressed = False
            self.press_sound_played = False
                
        # Draw the text
        text_surface = self.font.render(self.text, True, self.font_color)
        surface.blit(text_surface, (self.rect.centerx - text_surface.get_width() / 2, 
                                    self.rect.centery - text_surface.get_height() / 2))
    
    def is_pressed_hold(self):
        action = False
        # Mouse position
        pos = pygame.mouse.get_pos()
        
        # Check for button press
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                
                # Don't update self.clicked here to avoid recursion issues
                # with sound effects that might be triggered elsewhere
        
        return action
    


    def is_clicked_once(self):

        action = False
        #mouse position
        pos = pygame.mouse.get_pos()
        
        #mouse hover and clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1  and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action
    
    def set_hover_sound(self, sound_file):
        """Set or change the hover sound"""
        try:
            self.hover_sound = pygame.mixer.Sound(sound_file)
        except:
            print(f"Warning: {sound_file} not found")
            self.hover_sound = None
    
    def set_press_sound(self, sound_file):
        """Set or change the press sound"""
        try:
            self.press_sound = pygame.mixer.Sound(sound_file)
        except:
            print(f"Warning: {sound_file} not found")
            self.press_sound = None
    
    def clickForMusic(self, music):
        """Play a specific sound when clicked (use this for special one-time actions)"""
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return False
            
        if not pygame.mouse.get_pressed()[0] == 1 or self.clicked:
            return False
            
        # If we get here, it's a valid click
        self.clicked = True
        
        # Try to play the specified sound
        try:
            selectedMusic = pygame.mixer.Sound(music)
            selectedMusic.play()
            return True
        except:
            print(f"Warning: {music} not found")
            return False