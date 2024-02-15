import pygame
from utils import BACKDROUND_COLOR, BLUE_BG_COLOR, LABEL_COLOR, BLUE_LABEL, def_font

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
        
    def pop_up_message(self, theme, message_text, buttons):
        width = 300
        height = 300
        x,y = (100, 100)
        
        font = pygame.font.SysFont(def_font, 40)
        color = LABEL_COLOR if theme == "pink" else BLUE_LABEL
        text = font.render(message_text,True, color)
        text_x = x + (width - text.get_width()) // 2
        color = BACKDROUND_COLOR if theme == "pink" else BLUE_BG_COLOR
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        self.screen.blit(text, (text_x, 200))
        print(self.screen.get_at((text_x + 5, 200)) == LABEL_COLOR)
        for button in buttons:
            button.display_button(self.screen)
    
    def clear_rect(self, color, dimensions, coordinates):
        self.background_color = BACKDROUND_COLOR if color == "pink" else BLUE_BG_COLOR
        left, top = coordinates
        width, height = dimensions
        self.screen.fill(self.background_color, pygame.Rect(left, top, width, height))

    def clear_screen(self, color):
        self.background_color = BACKDROUND_COLOR if color == "pink" else BLUE_BG_COLOR
        self.screen.fill(self.background_color)
        pygame.display.update()
        
    
    