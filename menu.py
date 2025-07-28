import pygame


class Menu:
    def __init__(self, largura, altura):
        self.rodando = True
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont(None, 48)
        self.fonte_pequena = pygame.font.SysFont(None, 36)

    def desenhar(self, tela):
        tela.fill((0, 0, 0))  # Fundo preto

        titulo = self.fonte.render("WORMHOLE", True, (255, 255, 255))
        tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))

        rect_start = pygame.rect.Rect(300, 250, 200, 50)
        rect_quit = pygame.rect.Rect(350, 320, 100, 30)

        pygame.draw.rect(tela, (0, 150, 100), rect_start)
        pygame.draw.rect(tela, (150, 0, 0), rect_quit)
        # Opções
        opcoes = [
            "Start/Resume",
            "Sair"
        ]

        for i, opcao in enumerate(opcoes):
            texto = self.fonte_pequena.render(opcao, True, (255, 255, 255))
            tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, 265 + i * 60))

    @staticmethod
    def processar_eventos():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = evento.pos
                if (300 < click_x < 500) and (185 < click_y < 235):
                    return "fase1"
                elif (350 < click_x < 450) and (247 < click_y < 277):
                    return "sair"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "sair"
                elif evento.key == pygame.K_1:
                    return "fase1"
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
