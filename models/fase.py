import pygame
import pytmx
from models import spritesheet, player, body
from settings import LARGURA, ALTURA, VEL_PULO, VEL_PLAYER


class Fase:
    def __init__(self, arquivo_mapa):
        self.tmx_data = pytmx.load_pygame(arquivo_mapa)
        self.collision_rects = self.carregar_colisoes()
        self.concluded = False
        self.next_level = "menu"
        self.message =""

        #As cores são inicializadas aqui e alteradas em cada subclasse conforme escolhido para cada fase
        self.background_color = (0,0,0)
        self.bloco_color=(255,255,255)

        # Sprites
        self.background = pygame.rect.Rect(0,0,LARGURA,ALTURA)
        sprite_sheet_img = pygame.image.load("assets/Virtual Guy/Idle (32x32).png").convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_img)
        self.frame_0 = sprite_sheet.get_image(0, 32, 32, 2, False)
        self.frame_0_flipado = sprite_sheet.get_image(0, 32, 32, 2, True)

        # Inicializa objetos
        self.bloco = body.Body(pygame.rect.Rect(100,100,50,50), 100, 400, 64, 64, self.collision_rects)
        self.player = player.Player(self.frame_0, 300, 300, self.collision_rects)
        self.portal = body.Body(pygame.rect.Rect(100,100,50,70), 100, 400, 64, 64, self.player)

        self.rodando = True
        self.cor_fundo = (255, 255, 255)

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
        if self.player.rect.colliderect(self.portal.rect):
            return "next"
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
        messagem =pygame.font.SysFont(None, 48).render(self.message, True, (255, 255, 255))

        #Desenha fundo
        pygame.draw.rect(tela,self.background_color,self.background)
        # Desenhar mapa (igual ao seu código)
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        tela.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

        # Desenhar objetos
        tela.blit(messagem, (LARGURA/2-messagem.get_width()/2,100))
        tela.blit(self.player.texture, (self.player.rect.left, self.player.rect.top))
        pygame.draw.rect(tela,self.bloco_color,self.bloco.rect)
        pygame.draw.rect(tela, (5, 200, 50), self.portal.rect)

    def executar(self, tela):
        clock = pygame.time.Clock()

        while not self.concluded:
            resultado = self.processar_eventos()
            if resultado == "menu" or resultado == "sair":
                return resultado
            elif resultado == "next":
                return self.next_level

            self.atualizar()
            self.desenhar(tela)
            pygame.display.flip()
            clock.tick(60)