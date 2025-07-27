import time
import os
import pygame
from pygame.locals import *
from models import spritesheet, player, body
from settings import LARGURA, ALTURA, GRAVIDADE, VEL_MAX_CAIDA, VEL_PULO, VEL_PLAYER

import pytmx

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Wormhole")
clock = pygame.time.Clock()

tmx_data = pytmx.load_pygame("assets/Mapa/mapa01.tmx")

# Função para coletar colisões da Object Layer com propriedade "collidable"
def carregar_colisoes(tmx_data):
    colisoes = []

    layer = tmx_data.get_layer_by_name("ground")
    if isinstance(layer, pytmx.TiledTileLayer) and layer.properties.get("collidable", False):
        print(f"Processando layer collidable: {layer.name}")
        print("fds"+str(tmx_data.get_tile_properties_by_gid(7)))
        # Processa todos os tiles não-vazios
        for x, y, gid in layer:
            if gid != 0:  # Tile não vazio
                # Verifica se o tile tem propriedade collidable
                tile_props = tmx_data.get_tile_properties_by_gid(gid)
                if tile_props and tile_props.get("collidable", True):
                    colisoes.append(pygame.Rect(
                        x * tmx_data.tilewidth,
                        y * tmx_data.tileheight,
                        tmx_data.tilewidth,
                        tmx_data.tileheight
                    ))

    return colisoes


collision_rects = carregar_colisoes(tmx_data)
print(f"Total de colisões carregadas: {len(collision_rects)}")
# Cores
BRANCO = (255, 255, 255)
AZUL = (50, 100, 255)
VERMELHO = (255, 50, 50)

# Sprites
sprite_sheet_image = pygame.image.load("assets/Virtual Guy/Idle (32x32).png").convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
frame_0 = sprite_sheet.get_image(0, 32, 32, 2, True)

# Corpos
bloco = body.Body(frame_0, 100, 400, 64, 64, collision_rects)
player = player.Player(frame_0, 300, 300, collision_rects)

def desenhar_mapa(tela, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    tela.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))


def carregar_colisoes(tmx_data):
    colisoes = []

    # Verifica objetos com propriedade "collidable"
    for obj in tmx_data.objects:
        if obj.properties.get("collidable"):
            colisoes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    # Verifica tiles em camadas com propriedade "collidable"
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_props = tmx_data.get_tile_properties_by_gid(gid)
                if tile_props and tile_props.get("collidable"):
                    colisoes.append(pygame.Rect(
                        x * tmx_data.tilewidth,
                        y * tmx_data.tileheight,
                        tmx_data.tilewidth,
                        tmx_data.tileheight
                    ))

    return colisoes

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
    elif teclas[K_RIGHT] or teclas[K_d]:
        player.mover(VEL_PLAYER, bloco)
    else:
        player.vel_x = 0

    # Teleporte
    if player.teleportando:
        player.rect.left, player.rect.top, bloco.rect.left, bloco.rect.top = bloco.rect.left, bloco.rect.top, player.rect.left, player.rect.top
        player.teleportando = False

    # Atualizar física
    player.update_fisica(collision_rects + [bloco.rect])
    bloco.update_fisica(collision_rects + [player.rect])

    if bloco.rect.left== 0 or bloco.rect.right==LARGURA:
        player.vel_x = 0

    # Desenho
    desenhar_mapa(tela, tmx_data)
    pygame.draw.rect(tela, AZUL, player.rect)
    tela.blit(frame_0, (player.rect.left, player.rect.top))
    pygame.draw.rect(tela, VERMELHO, bloco.rect)
    #print(collision_rects)

    for colidder in collision_rects:
        pygame.draw.rect(tela, (0, 255, 0), colidder, 1)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
