import pygame
from utils import BACKDROUND_COLOR, BLUE_BG_COLOR

class ScreenHandler:
    
    screen = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls.screen:
            cls.screen = super().__new__(cls)
            cls._initialized = False
        return cls.screen
    
    def __init__(self, width, height, caption, bg_color):
         if not self._initialized:
            self.background_color = bg_color
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(caption)
            self.screen.fill(self.background_color)
            self._initialized = True
        
    def clear_screen(self, color):
        if color == "pink":
            self.background_color = BACKDROUND_COLOR
        elif color == "blue":
            self.background_color = BLUE_BG_COLOR
        self.screen.fill(self.background_color)
        pygame.display.update()

    
    