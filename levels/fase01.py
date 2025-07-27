import pygame
from models.fase import Fase


class Fase1(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa01.tmx")
        self.largura = largura
        self.altura = altura

        # Ajuste de posições iniciais específicas para esta fase
        self.player.rect.x = 300
        self.player.rect.y = 300
        self.bloco.rect.x = 100
        self.bloco.rect.y = 400

    def executar(self, tela):
        clock = pygame.time.Clock()
        self.rodando = True

        while self.rodando:
            resultado = self.processar_eventos()
            if resultado == "menu" or resultado == "sair":
                return resultado

            self.atualizar()
            self.desenhar(tela)
            pygame.display.flip()
            clock.tick(60)

        return "sair"