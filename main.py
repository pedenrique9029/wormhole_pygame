import pygame
from menu import Menu
from levels.fase01 import Fase1
from levels.fase02 import Fase2
from levels.fase03 import Fase3
from fim import Fim
from models.cutscene import Cutscene
from settings import LARGURA, ALTURA
import gerenciador_estados

# Inicializa a tela
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Wormhole")
pygame.display.set_icon(pygame.image.load("assets/portal_icon.png"))
clock = pygame.time.Clock()

# Carrega a trilha sonora
pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/menu_sound.mp3")
pygame.mixer.music.set_volume(0.75)
pygame.mixer.music.play(-1)

# Estados do jogo
gerenciador_estados.estados = {
    "menu": Menu(LARGURA, ALTURA),
    "cutscene": Cutscene(LARGURA, ALTURA),
    "fase1": Fase1(LARGURA, ALTURA),
    "fase2": Fase2(LARGURA, ALTURA),
    "fase3": Fase3(LARGURA, ALTURA),
    "fim": Fim(LARGURA, ALTURA),
}
rodando = True
while rodando:
    # Executa o estado atual
    resultado = gerenciador_estados.estados[gerenciador_estados.estado_atual].executar(tela)
    if resultado=="sair":
        rodando = False
    else:
        gerenciador_estados.estado_atual = resultado
    clock.tick(60)

pygame.quit()