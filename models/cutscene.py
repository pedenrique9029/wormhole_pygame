import pygame
import time

class Cutscene:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.rodando = True
        self.fonte = pygame.font.Font(None, 32)
        self.fonte_grande = pygame.font.Font(None, 60)
        self.texto_cutscene = [
            "Você é um cientista realizando experimentos num acelerador de partículas",
            "Quando repentinamente...",
            "PUFF!!!",
            "Você foi mandado para uma outra dimensão.",
            "Há um Tesseract de comportamento esquisito", 
            "Você consegue trocar de posição no espaço tempo através de uma ligação quântica.",
            "Há também, um portal que leva a outra dimensão.",
            "Você sai desesperadamente transitando entre as dimensões em busca de encontrar a sua de origem."
        ]
        self.imagem_fundo = pygame.image.load("assets/fundo_cutscene_pixelado.jpg")
        self.velocidade_texto = 50  # caracteres por segundo

    def executar(self, tela):
        pygame.mixer.music.load("assets/sounds/cutscene_sound.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        for frase in self.texto_cutscene:
            self.desenhar(tela, frase)
            resultado = self.atualizar()
            tela.fill((0, 0, 0))
            if resultado == "sair":
                return "sair"
            
        pygame.mixer.music.load("assets/sounds/soundtrack.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        return "fase1"

    def desenhar(self, tela, texto):
        tela.blit(self.imagem_fundo, (0,0))
        texto_renderizado = ''
        tempo_inicial = time.time()

        while len(texto_renderizado) < len(texto):
            tempo_passado = time.time() - tempo_inicial
            num_caracteres = min(int(tempo_passado * self.velocidade_texto), len(texto))
            texto_renderizado = texto[0:num_caracteres]

            tela.blit(self.imagem_fundo, (-120, -60))  # redesenha o fundo
            texto_surface = self.fonte.render(texto_renderizado, True, (255, 255, 255))
            tela.blit(texto_surface, (self.largura // 2 - texto_surface.get_width() // 2, self.altura // 2))

            pygame.display.flip()
            pygame.event.pump()
            pygame.time.delay(30)

    def atualizar(self):
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False
