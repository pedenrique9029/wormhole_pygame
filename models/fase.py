import pygame
import pytmx
from models import spritesheet, player, body, portal
from settings import LARGURA, ALTURA, VEL_PULO, VEL_PLAYER


class Fase:
    def __init__(self, arquivo_mapa, imagem_fundo):
        self.clock = pygame.time.Clock()
        self.tmx_data = pytmx.load_pygame(arquivo_mapa)
        self.collision_rects = self.carregar_colisoes()
        self.concluded = False
        self.next_level = "menu"
        self.message =""
        self.imagem_fundo = pygame.image.load(imagem_fundo)

        # Carrega efeito sonoro de teleporte
        self.teleport_sound = pygame.mixer.Sound("assets/sounds/teleport_sound_effect.mp3")
        self.teleport_sound.set_volume(0.1)

        #As cores são inicializadas aqui e alteradas em cada subclasse conforme escolhido para cada fase
        self.bloco_color = (255, 255, 255)

        # Sprite Player
        self.background = pygame.rect.Rect(0,0,LARGURA,ALTURA)

        #Sprite Botão
        botao_spritesheet_img = pygame.image.load("assets/botao.png").convert_alpha()
        botao_sprite_sheet = spritesheet.SpriteSheet(botao_spritesheet_img)
        self.botao_frame_0 = botao_sprite_sheet.get_image(0, 16, 16, 4, False)
        self.botao_frame_clickado = botao_sprite_sheet.get_image(1, 16, 16, 4, False)

        # Inicializa objetos
        self.bloco = body.Body(pygame.rect.Rect(100,100,50,50), 100, 400, 64, 64, self.collision_rects,True)
        self.player = player.Player(None, 300, 300, self.collision_rects)
        self.portal = portal.Portal(None, 1210, 400, [self.player])
        self.botao = body.Body(self.botao_frame_0,100,400, 64,32, [self.player,self.bloco],False)

    def carregar_colisoes(self):
        colisores = []
        # Carrega a colisão com o mapa
        for x, y, gid in self.tmx_data.get_layer_by_name("ground"):
            tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
            if tile_props and tile_props.get("collidable", False):
                colisores.append(pygame.Rect(
                    x * self.tmx_data.tilewidth,
                    y * self.tmx_data.tileheight,
                    self.tmx_data.tilewidth,
                    self.tmx_data.tileheight
                ))
        return colisores

    def processar_eventos(self):
        #O portal tem que estar visível para ser utilizado
        if self.player.rect.colliderect(self.portal.rect) and self.portal.visible:
            return "next"

        # Verifica se há botão visível na fase
        # (quando desejar que a fase não tenha tal mecanismo basta passar visible como False)
        if self.botao.visible:
            if self.botao.rect.colliderect(self.player) or self.botao.rect.colliderect(self.bloco):
                self.botao.texture = self.botao_frame_clickado
                # Torna o portal visivel caso não esteja
                if not self.portal.visible:
                    self.botao_color = (0,255,50)
                    self.portal.visible = True
            else:
                self.botao.texture = self.botao_frame_0
                self.botao_color = (150,150,150)
                self.portal.visible = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            if evento.type == pygame.KEYDOWN:
                if (evento.key == pygame.K_SPACE or evento.key == pygame.K_w or evento.key == pygame.K_UP) and self.player.no_chao:
                    self.player.vel_y = VEL_PULO
                    self.player.no_chao = False
                if (evento.key == pygame.K_s or evento.key == pygame.K_DOWN)  and not self.player.teleportando:
                    self.player.teleportando = True
        return None

    def atualizar(self):
        # Movimento horizontal
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.player.flip = True
            self.player.mover(-VEL_PLAYER, self.bloco)
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.player.flip = False
            self.player.mover(VEL_PLAYER, self.bloco)
        else:
            self.player.vel_x = 0

        # Teleporte
        if self.player.teleportando:
            self.teleport_sound.play()
            self.player.rect.topleft,self.bloco.rect.topleft = self.bloco.rect.topleft, self.player.rect.topleft
            self.player.teleportando = False

        # Atualiza animações
        dt = self.clock.tick(60)
        self.portal.animar()
        self.player.animar()
        self.player.atualizar_frame(dt)

        # Atualiza física dos objetos
        self.player.atualizar_fisica(self.collision_rects + [self.bloco.rect])
        self.bloco.atualizar_fisica(self.collision_rects + [self.player.rect])

        # Se o player tiver empurrando o bloco contra a borda da tela, impede o movimento
        if self.bloco.rect.left == 0 or self.bloco.rect.right == LARGURA:
            self.player.vel_x = 0

    def desenhar(self, tela):
        # Desenha fundo
        tela.blit(self.imagem_fundo, (0,0))
        # Desenhar tilemap
        for x, y, gid in self.tmx_data.get_layer_by_name("ground"):
            tile = self.tmx_data.get_tile_image_by_gid(gid)
            if tile:
                tela.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

    # Desenhar objetos
        if self.botao.visible:
            #Desenha o botão quando visível
            tela.blit(self.botao.texture, (self.botao.rect.left, self.botao.rect.top))
        if self.portal.visible:
            #Desenha o portal quando visível
            tela.blit(self.portal.texture, (self.portal.rect.left, self.portal.rect.top))
        # Desenha o player
        tela.blit(self.player.texture, (self.player.rect.left, self.player.rect.top))
        #Desenha o Bloco
        pygame.draw.rect(tela,self.bloco_color,self.bloco.rect, border_radius=7)
        if self.message:
            #Desenha somente se houver uma messagem
            messagem = pygame.font.SysFont(None, 48).render(self.message, True, (255, 255, 255))
            tela.blit(messagem, (LARGURA/2-messagem.get_width()/2,200))

    def executar(self, tela):
        clock = pygame.time.Clock()

        while not self.concluded:
            resultado = self.processar_eventos()
            if resultado == "sair":
                return resultado
            elif resultado == "next":
                return self.next_level

            self.atualizar()
            self.desenhar(tela)
            pygame.display.flip()
            clock.tick(60)