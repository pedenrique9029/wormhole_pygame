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

        # Título
        titulo = self.fonte.render("WORMHOLE", True, (255, 255, 255))
        tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))

        # Opções
        opcoes = [
            "1 - Start/Resume",
            "ESC - Sair"
        ]

        for i, opcao in enumerate(opcoes):
            texto = self.fonte_pequena.render(opcao, True, (255, 255, 255))
            tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, 200 + i * 50))

    @staticmethod
    def processar_eventos():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
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
