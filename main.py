import pygame
from menu import Menu
from levels.fase01 import Fase1
from levels.fase02 import Fase2
from levels.fase03 import Fase3
from settings import LARGURA, ALTURA
import gerenciador_estados

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Wormhole")
clock = pygame.time.Clock()

# Estados do jogo
gerenciador_estados.estados = {
    "menu": Menu(LARGURA, ALTURA),
    "fase1": Fase1(LARGURA, ALTURA),
    "fase2": Fase2(LARGURA, ALTURA),
    "fase3": Fase3(LARGURA, ALTURA),
}
rodando = True
while rodando:
    resultado = gerenciador_estados.estados[gerenciador_estados.estado_atual].executar(tela)
    if resultado=="sair":
        rodando = False
    else:
        gerenciador_estados.estado_atual = resultado
    clock.tick(60)

pygame.quit()
