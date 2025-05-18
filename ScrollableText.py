import pygame
from colors import Colors

class ScrollableTextArea:
    def __init__(self, x, y, width, height, top_left, top_right, bottom_left, bottom_right, font_size=23, max_lines=1, default_text_color=Colors.BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont("Roboto", font_size)
        self.default_text_color = default_text_color
        self.lines = []  # Will store lists of (word, color) tuples for each line
        self.max_lines = max_lines
        self.scroll_offset = 0
        self.max_visible_lines = 16 # Approximate based on font size
        self.top_left = top_left
        self.top_right = top_right
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right
    
    def add_text(self, text, color=None, highlight_words=None):
    
        if color is None:
            color = self.default_text_color
        
        if highlight_words is None:
            highlight_words = {}
            
        self.max_lines += 1
        new_lines = text.split('\n')
        
        # Process each line
        for line in new_lines:
            # Split the line into words
            words = line.split()
            styled_line = []
            
            if not words:  # Handle empty lines
                self.lines.append([(line, color)])
                continue
                
            # Create a list of (word, color) tuples for this line
            for word in words:
                # Check if this word should be highlighted
                word_color = color
                for highlight_word, highlight_color in highlight_words.items():
                    # Check if this word matches the highlight word (case-insensitive)
                    if word.lower() == highlight_word.lower() or word.lower().startswith(highlight_word.lower() + ",") or word.lower().startswith(highlight_word.lower() + "."):
                        word_color = highlight_color
                        break
                
                styled_line.append((word, word_color))
            
            self.lines.append(styled_line)
        
        # Keep only the last max_lines
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]
        
        # Auto-scroll to bottom
        if len(self.lines) > self.max_visible_lines:
            self.scroll_offset = len(self.lines) - self.max_visible_lines
    
    def clear(self):
        self.lines = []
        self.scroll_offset = 0
    
    def scroll_up(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
    
    def scroll_down(self):
        if self.scroll_offset < len(self.lines) - self.max_visible_lines:
            self.scroll_offset += 1
    
    def handle_mouse_wheel(self, event):
        """Handle mouse wheel scrolling when mouse is over the text area.
        
        Args:
            event: Pygame event (should be MOUSEWHEEL type)
        
        Returns:
            bool: True if event was handled, False otherwise
        """
        # Check if mouse is over the text area
        mouse_pos = pygame.mouse.get_pos()
        if not self.rect.collidepoint(mouse_pos):
            return False
            
        # Handle scrolling
        if event.y > 0:  # Scroll up
            self.scroll_up()
        elif event.y < 0:  # Scroll down
            self.scroll_down()
            
        return True
    
    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, Colors.LIGHT_BLUE, self.rect, 0, 
                        border_top_left_radius=self.top_left, 
                        border_top_right_radius=self.top_right, 
                        border_bottom_left_radius=self.bottom_left, 
                        border_bottom_right_radius=self.bottom_right)
        
        pygame.draw.rect(surface, Colors.BLACK, self.rect, 2, 
                        border_top_left_radius=self.top_left, 
                        border_top_right_radius=self.top_right, 
                        border_bottom_left_radius=self.bottom_left, 
                        border_bottom_right_radius=self.bottom_right)
        
        # Calculate visible lines
        start_idx = self.scroll_offset
        end_idx = min(start_idx + self.max_visible_lines, len(self.lines))
        
        # Draw text with their individual colors
        y_offset = self.rect.y + 20
        for i in range(start_idx, end_idx):
            line = self.lines[i]
            x_offset = self.rect.x + 10
            
            # Draw each word with its specific color
            for word, color in line:
                word_surface = self.font.render(word, True, color)
                surface.blit(word_surface, (x_offset, y_offset))
                x_offset += word_surface.get_width() + self.font.size(' ')[0]  # Add space between words
            
            y_offset += self.font.get_height() + 2
        
        # Draw scroll indicators if needed
        if len(self.lines) > self.max_visible_lines:
            if self.scroll_offset > 0:
                # Up arrow
                pygame.draw.polygon(surface, Colors.BLACK, [
                    (self.rect.right - 15, self.rect.y + 10),
                    (self.rect.right - 5, self.rect.y + 10),
                    (self.rect.right - 10, self.rect.y + 5)
                ])
            
            if self.scroll_offset < len(self.lines) - self.max_visible_lines:
                # Down arrow
                pygame.draw.polygon(surface, Colors.BLACK, [
                    (self.rect.right - 15, self.rect.bottom - 10),
                    (self.rect.right - 5, self.rect.bottom - 10),
                    (self.rect.right - 10, self.rect.bottom - 5)
                ])