import pygame
from settings import GRAVIDADE, VEL_MAX_CAIDA
from settings import LARGURA,ALTURA


class Body:
    def __init__(self, texture, x, y, width, height, colisores):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.colisores = colisores
        self.texture = texture
        self.screen_width = LARGURA
        self.screen_height = ALTURA
        self.no_chao = False

    def update_fisica(self, plataformas):
        # Aplica gravidade
        self.vel_y = min(self.vel_y + GRAVIDADE, VEL_MAX_CAIDA)

        # Movimento horizontal
        self.rect.x += self.vel_x
        self._check_horizontal_collision(plataformas)
        self._check_screen_bounds_horizontal()

        # Movimento vertical
        self.rect.y += self.vel_y
        self._check_vertical_collision(plataformas)
        self._check_screen_bounds_vertical()

    def _check_horizontal_collision(self, plataformas):
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.vel_x > 0:  # Movendo para direita
                    self.rect.right = plataforma.left
                elif self.vel_x < 0:  # Movendo para esquerda
                    self.rect.left = plataforma.right
                self.vel_x = 0  # Para o movimento horizontal ao colidir

    def _check_vertical_collision(self, plataformas):
        self.no_chao = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.vel_y > 0:  # Caindo
                    self.rect.bottom = plataforma.top
                    self.no_chao = True
                elif self.vel_y < 0:  # Subindo (colidiu com teto)
                    self.rect.top = plataforma.bottom
                self.vel_y = 0  # Reseta a velocidade ao tocar algo

    def _check_screen_bounds_horizontal(self):
        # Impede sair pela esquerda
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0

        # Impede sair pela direita
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.vel_x = 0

    def _check_screen_bounds_vertical(self):
        # Impede sair por cima
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        # Impede sair por baixo (opcional - depende do seu jogo)
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height
            self.vel_y = 0
            self.no_chao = True