import pygame
from colors import Colors
# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen")

# Colors
BACKGROUND = (30, 30, 30)
BAR_BORDER = (150, 150, 150)
BAR_BACKGROUND = (60, 60, 60)
BAR_FILL = (75, 105, 255)
TEXT_COLOR = (220, 220, 220)

# Fonts
font = pygame.font.SysFont('Roboto', 36)
small_font = pygame.font.SysFont('Roboto', 24)

class LoadingBar:
    def __init__(self, x, y, width, height, max_value=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_value = max_value
        self.value = 0
        self.border_width = 2
        
    def update(self, value):
        self.value = min(value, self.max_value)
        
    def draw(self, surface):
        # Draw border/background
        pygame.draw.rect(surface, Colors.LIGHT_BEIGE, 
                        (self.x - self.border_width, 
                        self.y - self.border_width, 
                        self.width + self.border_width * 2, 
                        self.height + self.border_width * 2), border_radius=5)
        # Draw dark background
        pygame.draw.rect(surface,Colors.LIGHT_BEIGE, 
                        (self.x, self.y, self.width, self.height))
        
        # Draw the filled portion
        fill_width = int((self.value / self.max_value) * self.width)
        if fill_width > 0:
            pygame.draw.rect(surface, "#11728C", 
                            (self.x, self.y, fill_width, self.height), border_radius=5)
        
        # Draw percentage text
        percentage = f"{int(self.value / self.max_value * 100)}%"
        text = font.render(percentage, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, self.y + self.height // 2))
        #surface.blit(text, text_rect)
        
        # Draw "Loading..." text
        loading_text = small_font.render("Loading...", True, TEXT_COLOR)
        loading_rect = loading_text.get_rect(midbottom=(WIDTH // 2, self.y - 10))
        "surface.blit(loading_text, loading_rect)"