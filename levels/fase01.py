import pygame
import pytmx
from models.fase import Fase
import gerenciador_estados


class Fase1(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa01.tmx")
        self.next_level="fase2"
        self.message = 'Pressione "J" para trocar de posição com bloco'
        self.largura = largura
        self.altura = altura

        #Ajuste da Paleta de cores
        self.background_color = (20,50,100)
        self.bloco_color = (250,150,20)

        # Ajuste de posições iniciais específicas para esta fase
        self.portal.rect.x = 1250
        self.portal.rect.y = 288
        self.player.rect.x = 300
        self.player.rect.y = 800
        self.bloco.rect.x = 200
        self.bloco.rect.y = 800