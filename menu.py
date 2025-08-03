import pygame
from settings import LARGURA, ALTURA

class Menu:
    def __init__(self, largura, altura):
        self.rodando = True
        self.largura = largura
        self.altura = altura
        self.fonte_grande = pygame.font.SysFont(None, 52)
        self.fonte = pygame.font.SysFont(None, 48)
        self.fonte_pequena = pygame.font.SysFont(None, 36)
        self.rect_start = pygame.rect.Rect(LARGURA/2-100, ALTURA/2-20, 200, 50)
        self.rect_quit = pygame.rect.Rect(LARGURA/2-50, ALTURA/2+67, 100, 30)

    def desenhar(self, tela):
        imagem_fundo  = pygame.image.load('assets/buraco_negro_pixelizado_espelhado.jpg')# Imagem de fundo
        imagem_fundo = pygame.transform.rotate(imagem_fundo, 90)
        tela.blit(imagem_fundo, (-120, -60))
        titulo = self.fonte_grande.render("WORMHOLE", True, (255, 255, 255))
        tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 220))

        pygame.draw.rect(tela, (0, 0, 0), self.rect_start)
        pygame.draw.rect(tela, (0, 0, 0), self.rect_quit)

        text_start = self.fonte.render("Iniciar Jogo", True, (255, 255, 255))
        tela.blit(text_start, (self.largura // 2 - text_start.get_width() // 2, 350))

        text_quit = self.fonte_pequena.render("Sair", True, (255, 255, 255))
        tela.blit(text_quit, (self.largura // 2 - text_quit.get_width() // 2, 420))

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = evento.pos
                if (self.rect_start.left < click_x < self.rect_start.right) and (self.rect_start.top < click_y < self.rect_start.bottom):
                    return "fase1"
                elif (self.rect_quit.left < click_x < self.rect_quit.right) and (self.rect_quit.top < click_y < self.rect_quit.bottom):
                    return "sair"
        return None

    def executar(self, tela):
        clock = pygame.time.Clock()
        while self.rodando:
            resultado = self.processar_eventos()
            if resultado:
                return resultado

            self.desenhar(tela)
            pygame.display.flip()
            clock.tick(60)
