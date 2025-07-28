import pygame
import pytmx
from models.fase import Fase
import gerenciador_estados


class Fase1(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa01.tmx")
        self.next_level="fase2"
        self.largura = largura
        self.altura = altura

        # Ajuste de posições iniciais específicas para esta fase
        self.portal.rect.x = 780
        self.portal.rect.y = 320
        self.player.rect.x = 300
        self.player.rect.y = 300
        self.bloco.rect.x = 100
        self.bloco.rect.y = 400