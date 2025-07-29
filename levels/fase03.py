import pygame
from models.fase import Fase


class Fase3(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa03.tmx","assets/imagem_fim_editada.jpg")
        self.largura = largura
        self.altura = altura
        self.next_level = "fim"

        # Ajuste da Paleta de cores
        self.background_color = (80,50,160)
        self.bloco_color = (200,180,50)

        # Necessário ativar o portal para avançar
        self.botao.visible = True

        # Ajuste de posições iniciais específicas para esta fase
        self.portal.rect.y = 416
        self.player.rect.x = 512
        self.player.rect.y = 304
        self.bloco.rect.x = 10
        self.bloco.rect.y = 320
        self.botao.rect.x = 552
        self.botao.rect.y = 576
