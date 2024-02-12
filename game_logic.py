import pygame

class GameLogic:
    
    def __init__(self, text_boxes, f_handler):
        self.text_boxes = text_boxes
        self.f_handler = f_handler
        
    def activate_box(self, position):
        for box in self.text_boxes:
            if box.collide_point(position):
                box.activate()
            else:
                box.deactivate()
        
    def handle_input(self, event, screen, theme):
        for box in self.text_boxes:
            if event.type == pygame.KEYDOWN and box.is_active():
                if event.key == pygame.K_BACKSPACE:
                    # Handle backspace key
                    box.text = box.text[:-1]
                elif event.unicode.isdigit() and (int(event.unicode) != 0):
                    # Append the pressed key to the text
                    box.text += event.unicode
                box.draw(screen, theme)
                self.f_handler.draw_borders(screen, theme)
                box.deactivate()
                
