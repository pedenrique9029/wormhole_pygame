import pygame
from pygame.locals import *

pygame.init()

# Tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Wormhole")
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
AZUL = (50, 100, 255)
VERMELHO = (255, 50, 50)
CINZA = (100, 100, 100)

# Constantes de física
GRAVIDADE = 0.5
VEL_MAX_CAIDA = 10
vel_player = 5

# Objetos
player = pygame.Rect(100, 100, 50, 50)
bloco = pygame.Rect(200, 100, 50, 50)
chao = pygame.Rect(0, ALTURA - 50, LARGURA, 50)

#Controladores de Mecanicas
teleportando = False
pulando = False
no_chao = True

# Velocidade vertical dos corpos
vel_y_player = 0
vel_y_bloco = 0

def aplicar_gravidade(rect, vel_y, colisor):
    vel_y += GRAVIDADE
    vel_y = min(vel_y, VEL_MAX_CAIDA)
    rect.y += vel_y

    if rect.colliderect(colisor):
        rect.bottom = colisor.top
        vel_y = 0
    return vel_y

def esta_em_cima(player, alvo):
    return (
        player.bottom >= alvo.top and
        player.bottom <= alvo.top + 10 and
        player.right > alvo.left and
        player.left < alvo.right
    )

def mover_player(dx):
    global player, bloco

    futuro_player = player.move(dx, 0)

    if not futuro_player.colliderect(bloco):
        player = futuro_player
    else:
        futuro_bloco = bloco.move(dx, 0)
        if (0 <= futuro_bloco.x <= LARGURA - bloco.width) and not futuro_bloco.colliderect(player):
            if bloco.bottom == chao.top:
                bloco.x += dx
                player = futuro_player

# Loop principal
rodando = True
while rodando:
    tela.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            rodando = False
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE and not pulando:
                pulando = True
                player.y -= 100
            if evento.key == K_j and not teleportando:
                teleportando = True

    # Entrada
    teclas = pygame.key.get_pressed()
    if player.right<LARGURA:
        can_move_right=True
    else:
        can_move_right=False
    if player.left>0:
        can_move_left=True
    else:
        can_move_left=False
    
    if teclas[K_LEFT] or teclas[K_a] and can_move_left:
        mover_player(-vel_player)
    if teclas[K_RIGHT] or teclas[K_d] and can_move_right:
        mover_player(vel_player)

    if teleportando:
        direction_teleport = bloco.x,bloco.y
        player.x,player.y,bloco.x,bloco.y =direction_teleport[0],direction_teleport[1],player.x,player.y
        teleportando = False

    # Gravidade
    if esta_em_cima(player, bloco):
        player.bottom = bloco.top
        vel_y_player = 0
    elif esta_em_cima(player, chao):
        player.bottom = chao.top
        vel_y_player = 0
    else:
        vel_y_player = min(vel_y_player + GRAVIDADE, VEL_MAX_CAIDA)
        player.y += vel_y_player
    
    if esta_em_cima(bloco, player):
        bloco.bottom = player.top
    elif esta_em_cima(bloco, chao):
        bloco.bottom = chao.top
    else:
        vel_y_bloco = aplicar_gravidade(bloco, vel_y_bloco, chao)

    if esta_em_cima(player,chao) or esta_em_cima(player, bloco):
        pulando = False

    pygame.draw.rect(tela, CINZA, chao)
    pygame.draw.rect(tela, AZUL, player)
    pygame.draw.rect(tela, VERMELHO, bloco)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
