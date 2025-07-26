import pygame
from models.body import Body
from pygame.locals import *
from settings import LARGURA, VEL_PULO, GRAVIDADE, VEL_MAX_CAIDA


class Player(Body):
    def __init__(self, x, y, colisores):
        super().__init__(x, y, 64, 64, colisores)
        self.pulando = False
        self.teleportando = False
        self.no_chao = False  # Adicionando o atributo que estava faltando
        self.vel_y = 0  # Adicionando também a velocidade vertical

    def mover(self, dx, bloco):
        futuro = self.rect.move(dx, 0)

        # Verifica colisão com o bloco
        if futuro.colliderect(bloco.rect):
            # Verifica se está tentando mover o bloco
            if dx > 0:  # Movendo para direita
                if all(not bloco.rect.move(dx, 0).colliderect(c) for c in self.colisores if c != bloco.rect):
                    bloco.rect.x += dx
                    self.rect.x += dx
            elif dx < 0:  # Movendo para esquerda
                if all(not bloco.rect.move(dx, 0).colliderect(c) for c in self.colisores if c != bloco.rect):
                    bloco.rect.x += dx
                    self.rect.x += dx
        else:
            # Movimento normal sem colisão
            self.rect.x += dx

        # Mantém o jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))

    def pular(self):
        if self.no_chao:
            self.vel_y = VEL_PULO
            self.no_chao = False
            self.pulando = True

    def update_fisica(self, colisores):
        # Aplicar gravidade
        self.vel_y += GRAVIDADE
        self.vel_y = min(self.vel_y, VEL_MAX_CAIDA)
        self.rect.y += self.vel_y

        # Resetar estado no_chao
        self.no_chao = False

        # Verificar colisões em todas as direções
        for obj_rect in colisores:
            if self.rect.colliderect(obj_rect):
                # Colisão vertical
                if self.vel_y > 0:  # Caindo
                    self.rect.bottom = obj_rect.top if hasattr(obj_rect, 'rect') else obj_rect.top
                    self.vel_y = 0
                    self.no_chao = True
                    self.pulando = False
                elif self.vel_y < 0:  # Subindo
                    self.rect.top = obj_rect.rect.bottom if hasattr(obj_rect, 'rect') else obj_rect.bottom
                    self.vel_y = 0
                # Colisão Lateral
                if self.vel_x > 0:  # Pra direita
                    self.rect.right = obj_rect.left
                    self.vel_y = 0
                elif self.vel_x < 0:  # Pra esquerda
                    self.rect.left = obj_rect.right
                    self.vel_y = 0
