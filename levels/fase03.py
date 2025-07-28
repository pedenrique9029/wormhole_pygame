import pygame
from models.fase import Fase


class Fase3(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa03.tmx")
        self.largura = largura
        self.altura = altura
        self.next_level = "menu"
        self.message = ""

        # Ajuste da Paleta de cores
        self.background_color = (80,50,160)
        self.bloco_color = (200,180,50)

        # Ajuste de posições iniciais específicas para esta fase
        self.portal.rect.x=1250
        self.portal.rect.y=560
        self.player.rect.x = 512
        self.player.rect.y = 560
        self.bloco.rect.x = 10
        self.bloco.rect.y = 304
