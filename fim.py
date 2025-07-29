import pygame

class Fim:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont(None, 60)
        self.rodando = True

    def desenhar(self, tela):
        tela.fill((0, 0, 0))  # Fundo preto

        texto = self.fonte.render("Parabéns! Você conseguiu!", True, (255, 255, 255))
        tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, 300))

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
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
