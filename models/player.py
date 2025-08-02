from models.body import Body
from settings import  VEL_PULO

class Player(Body):
    def __init__(self, texture, x, y, colisores):
        super().__init__(texture, x, y, 64, 64, colisores,True)
        self.pulando = False
        self.teleportando = False

    def mover(self, dx, bloco):
        futuro = self.rect.move(dx, 0)

        if futuro.colliderect(bloco.rect):
            # Verifica se pode empurrar o bloco
            pode_mover = True
            
            for c in self.colisores:
                if c != bloco.rect:
                    if bloco.rect.move(dx, 0).colliderect(c):
                        pode_mover = False
                        break

            if pode_mover:
                bloco.rect.x += dx
        else:
            self.vel_x = dx  # Atribui movimento horizontal

    def pular(self, bloco):
        if self.no_chao:
            self.vel_y = VEL_PULO
            self.no_chao = False
            self.pulando = True
            # Ajuste para evitar grudar em paredes/blocos
            if abs(self.rect.right - bloco.rect.left) < 5:  # Se estiver muito perto à direita
                self.rect.right = bloco.rect.left - 1
            elif abs(self.rect.left - bloco.rect.right) < 5:  # Se estiver muito perto à esquerda
                self.rect.left = bloco.rect.right + 1
