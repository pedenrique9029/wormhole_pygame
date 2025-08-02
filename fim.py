import pygame

class Fim:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fonte = pygame.font.SysFont(None, 60)
        self.rodando = True

    def desenhar(self, tela):
        imagem_fundo = pygame.image.load('assets/imagem_fim_editada.jpg')  # Imagem de fundo
        tela.blit(imagem_fundo, (-170, -100))

        texto = self.fonte.render("Parabéns! Você conseguiu!", True, (255, 255, 255))
        tela.blit(texto, (self.largura // 2 - texto.get_width() // 2, 300))

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "sair"
        return None

    def executar(self, tela):
        clock = pygame.time.Clock()
        pygame.mixer.music.stop()  # Para a música do jogo
        musica_final = pygame.mixer.Sound("assets/sounds/victory_sound.mp3").play()  # Toca o som de vitória
        musica_final.set_volume(0.3)
        while self.rodando:
            resultado = self.processar_eventos()
            if resultado:
                return resultado

            self.desenhar(tela)
            pygame.display.flip()
            clock.tick(60)
