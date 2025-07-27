import pygame
from menu import Menu
from levels.fase01 import Fase1
from settings import LARGURA, ALTURA


pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Wormhole")
clock = pygame.time.Clock()

# Estados do jogo
estados = {
    "menu": Menu(LARGURA, ALTURA),
    "fase1": Fase1(LARGURA, ALTURA)
}

estado_atual = "menu"
rodando = True

while rodando:
    # Processa o estado atual
    if estado_atual == "menu":
        menu = estados["menu"]
        menu.desenhar(tela)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:  # Tecla 1 para iniciar
                    estado_atual = "fase1"
                elif evento.key == pygame.K_ESCAPE:
                    rodando = False

    elif estado_atual == "fase1":
        resultado = estados["fase1"].executar(tela)
        if resultado == "menu":
            estado_atual = "menu"
        elif resultado == "sair":
            rodando = False

    clock.tick(60)

pygame.quit()