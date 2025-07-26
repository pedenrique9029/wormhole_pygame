import pygame

class SpriteSheet:
    def __init__(self, sheet):
        self.sheet = sheet
    
    def get_image(self, frame, width, height, scale,flip_h):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame*width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        pygame.transform.flip(image, flip_h, False)
        image.set_colorkey((0, 0, 0)) 
        return image
