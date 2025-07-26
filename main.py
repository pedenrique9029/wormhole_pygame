import time

import pygame
from pygame.locals import *
from models import spritesheet, player, body
from settings import LARGURA, ALTURA, GRAVIDADE, VEL_MAX_CAIDA, VEL_PULO, VEL_PLAYER

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Wormhole")
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
AZUL = (50, 100, 255)
VERMELHO = (255, 50, 50)
CINZA = (100, 100, 100)

# Sprites
sprite_sheet_image = pygame.image.load("assets/Virtual Guy/Idle (32x32).png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
frame_0 = sprite_sheet.get_image(0, 32, 32, 2, True)

# Corpos
chao = pygame.Rect(0, ALTURA - 100, LARGURA-100, 50)
chao2 = pygame.Rect(LARGURA-100, ALTURA - 150, 100, 50)  # Plataforma elevada

bloco = body.Body(100, 400, 64, 64, [chao, chao2])
player = player.Player(300, 300, [chao, chao2])

# --- LOOP PRINCIPAL --- #

rodando = True
while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            rodando = False
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE and player.no_chao:
                player.vel_y = VEL_PULO
                player.no_chao = False
            if evento.key == K_j and not player.teleportando:
                player.teleportando = True

    # Movimento horizontal
    teclas = pygame.key.get_pressed()
    if teclas[K_LEFT] or teclas[K_a]:
        player.mover(-VEL_PLAYER, bloco)
    if teclas[K_RIGHT] or teclas[K_d]:
        player.mover(VEL_PLAYER, bloco)

    # Teleporte
    if player.teleportando:
        player.rect.left, player.rect.top, bloco.rect.left, bloco.rect.top = bloco.rect.left, bloco.rect.top, player.rect.left, player.rect.top
        player.teleportando = False

    # Atualizar física
    player.update_fisica([bloco.rect, chao, chao2])
    bloco.update_fisica([player.rect, chao, chao2])

    # Desenho
    pygame.draw.rect(tela, CINZA, chao)
    pygame.draw.rect(tela, CINZA, chao2)
    pygame.draw.rect(tela, AZUL, player.rect)
    tela.blit(frame_0, (player.rect.left, player.rect.top))
    pygame.draw.rect(tela, VERMELHO, bloco.rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()