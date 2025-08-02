import pygame
from settings import GRAVIDADE
from settings import LARGURA,ALTURA

class Body:
    def __init__(self, texture, x, y, width, height, colisores:list, visible):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.colisores = colisores
        self.texture = texture
        self.screen_width = LARGURA
        self.screen_height = ALTURA
        self.no_chao = False
        self.visible =  visible

    def atualizar_fisica(self, colisores):
        # Aplica gravidade
        self.vel_y+= GRAVIDADE
        # Movimento horizontal
        self.rect.x += self.vel_x
        self._check_horizontal_collision(colisores)
        self._check_screen_bounds_horizontal()

        # Movimento vertical
        self.rect.y += self.vel_y
        self._check_vertical_collision(colisores)

    def _check_horizontal_collision(self, colisores):
        for colisor in colisores:
            if self.rect.colliderect(colisor):
                if self.vel_x > 0:  # Movendo para direita
                    self.rect.right = colisor.left
                elif self.vel_x < 0:  # Movendo para esquerda
                    self.rect.left = colisor.right
                self.vel_x = 0  # Para o movimento horizontal ao colidir

    def _check_vertical_collision(self, colisores):
        self.no_chao = False
        for colisor in colisores:
            if self.rect.colliderect(colisor):
                if self.vel_y > 0:
                    self.rect.bottom = colisor.top
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.rect.top = colisor.bottom
                self.vel_y = 0  # Zera a velocidade ao tocar algo

    def _check_screen_bounds_horizontal(self):
        # Impede sair da tela horizontalmente
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.vel_x = 0