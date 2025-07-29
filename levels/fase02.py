import pygame
from models.fase import Fase


class Fase2(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa02.tmx")
        self.largura = largura
        self.altura = altura
        self.next_level = "fase3"
        self.message = "Ative o portal por meio do botão"

        # Ajuste da Paleta de cores
        self.background_color = (20, 100, 80)
        self.bloco_color = (150, 20, 120)

        #Necessário ativar o portal para avançar
        self.botao.visible=True

        # Ajuste de posições iniciais específicas para esta fase
        self.portal.rect.x=1250
        self.portal.rect.y=528
        self.player.rect.x = 300
        self.player.rect.y = 576
        self.bloco.rect.x = 10
        self.bloco.rect.y = 416
        self.botao.rect.x = 810
        self.botao.rect.y = 546
