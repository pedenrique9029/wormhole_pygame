import pygame

from settings import GRAVIDADE, VEL_MAX_CAIDA


import pygame

class Body:
    def __init__(self, x, y, width, height, colisores):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.colisores = colisores

    def update_fisica(self, colisores):
        # Aplicar gravidade
        self.vel_y += GRAVIDADE
        self.vel_y = min(self.vel_y, VEL_MAX_CAIDA)
        self.rect.y += self.vel_y
        
        # Verificar colisões
        for obj_rect in colisores:

            if self.rect.colliderect(obj_rect):
                # Colisão vertical
                if self.vel_y > 0:  # Caindo
                    self.rect.bottom = obj_rect.top
                    self.vel_y = 0
                elif self.vel_y < 0:  # Subindo
                    self.rect.top = obj_rect.bottom
                    self.vel_y = 0

