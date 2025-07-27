import pygame
import pytmx
from models import spritesheet, player, body
from settings import LARGURA, ALTURA, VEL_PULO, VEL_PLAYER


class Fase:
    def __init__(self, arquivo_mapa):
        self.tmx_data = pytmx.load_pygame(arquivo_mapa)
        self.collision_rects = self.carregar_colisoes()

        # Sprites
        sprite_sheet_img = pygame.image.load("assets/Virtual Guy/Idle (32x32).png").convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_img)
        self.frame_0 = sprite_sheet.get_image(0, 32, 32, 2, False)
        self.frame_0_flipado = sprite_sheet.get_image(0, 32, 32, 2, True)

        # Inicializa objetos (posições podem ser ajustadas por fase)
        self.bloco = body.Body(pygame.rect.Rect(100,100,50,50), 100, 400, 64, 64, self.collision_rects)
        self.player = player.Player(self.frame_0, 300, 300, self.collision_rects)

        self.rodando = True
        self.cor_fundo = (255, 255, 255)  # BRANCO

    def carregar_colisoes(self):
        colisoes = []
        # Mesma lógica de colisão do seu código original
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile_props and tile_props.get("collidable", False):
                        colisoes.append(pygame.Rect(
                            x * self.tmx_data.tilewidth,
                            y * self.tmx_data.tileheight,
                            self.tmx_data.tilewidth,
                            self.tmx_data.tileheight
                        ))
        return colisoes

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and self.player.no_chao:
                    self.player.vel_y = VEL_PULO
                    self.player.no_chao = False
                if evento.key == pygame.K_j and not self.player.teleportando:
                    self.player.teleportando = True
                if evento.key == pygame.K_ESCAPE:
                    return "menu"
        return None

    def atualizar(self):
        # Movimento horizontal (igual ao seu código)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.player.texture = self.frame_0_flipado
            self.player.mover(-VEL_PLAYER, self.bloco)
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.player.texture = self.frame_0
            self.player.mover(VEL_PLAYER, self.bloco)
        else:
            self.player.vel_x = 0

        # Teleporte
        if self.player.teleportando:
            self.player.rect.left, self.player.rect.top, self.bloco.rect.left, self.bloco.rect.top = \
                self.bloco.rect.left, self.bloco.rect.top, self.player.rect.left, self.player.rect.top
            self.player.teleportando = False

        # Atualizar física
        self.player.update_fisica(self.collision_rects + [self.bloco.rect])
        self.bloco.update_fisica(self.collision_rects + [self.player.rect])

        if self.bloco.rect.left == 0 or self.bloco.rect.right == LARGURA:
            self.player.vel_x = 0

    def desenhar(self, tela):
        tela.fill(self.cor_fundo)

        # Desenhar mapa (igual ao seu código)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tela.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

        # Desenhar objetos
        tela.blit(self.player.texture, (self.player.rect.left, self.player.rect.top))
        pygame.draw.rect(tela,(255,0,50),self.bloco.rect,)
        #tela.blit(self.bloco.texture, (self.bloco.rect.left, self.bloco.rect.top))

        #desenhar colisões (para debug)
        for colisor in self.collision_rects:
            pygame.draw.rect(tela, (0, 255, 0), colisor, 1)

    def executar(self, tela):
        clock = pygame.time.Clock()
        self.rodando = True

        while self.rodando:
            resultado = self.processar_eventos()
            if resultado:
                return resultado

            self.atualizar()
            self.desenhar(tela)
            pygame.display.update()
            clock.tick(60)