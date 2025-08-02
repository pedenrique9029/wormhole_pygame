from models.fase import Fase

class Fase1(Fase):
    def __init__(self, largura, altura):
        super().__init__("assets/Mapa/mapa01.tmx","assets/fundo_fase1.jpg")
        self.next_level="fase2"
        self.message = 'Pressione "S" ou "Down" para trocar de posição com bloco'
        self.largura = largura
        self.altura = altura

        #Ajuste da Paleta de cores
        self.bloco_color = (250,150,20)

        # Ajuste de posições iniciais específicas para esta fase
        self.portal.rect.y = 260
        self.player.rect.x = 300
        self.player.rect.y = 560
        self.bloco.rect.x = 200
        self.bloco.rect.y = 560