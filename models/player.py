import pygame
from models.body import Body
from models.spritesheet import SpriteSheet
from settings import  VEL_PULO

class Player(Body):
    def __init__(self, texture, x, y, colisores):
        super().__init__(texture, x, y, 64, 64, colisores,True)
        self.teleportando = False
        self.rect = pygame.Rect(0, 0, 64, 64) 
        self.flip = False
        # Carrega o spritesheet da animação Idle
        sprite_sheet_idle = SpriteSheet(pygame.image.load("assets\Virtual Guy\Idle (32x32).png"))
        # Animação Idle
        self.frames_idle = []
        for i in range(sprite_sheet_idle.sheet.get_width() // 32):
            self.frames_idle.append(sprite_sheet_idle.get_image(i,32,32,2,False))
        # Animação Idle Flipada
        self.frames_idle_flip = []
        for i in range(sprite_sheet_idle.sheet.get_width() // 32):
            self.frames_idle_flip.append(sprite_sheet_idle.get_image(i,32,32,2,True))

        # Carrega o spritesheet da animação Run
        sprite_sheet_run = SpriteSheet(pygame.image.load("assets\Virtual Guy\Run (32x32).png"))
        # Animação Run
        self.frames_run = []
        for i in range(sprite_sheet_run.sheet.get_width() // 32):
            self.frames_run.append(sprite_sheet_run.get_image(i,32,32,2,False))
        # Animação Run Flipada
        self.frames_run_flip = []
        for i in range(sprite_sheet_run.sheet.get_width() // 32):
            self.frames_run_flip.append(sprite_sheet_run.get_image(i,32,32,2,True))

        # Carrega o spritesheet da animação Jump
        sprite_sheet_jump = SpriteSheet(pygame.image.load("assets\Virtual Guy\Jump (32x32).png"))
        # Animação Jump
        self.frames_jump = []
        for i in range(sprite_sheet_jump.sheet.get_width() // 32):
            self.frames_jump.append(sprite_sheet_jump.get_image(i,32,32,2,False))
        # Animação Jump Flipada
        self.frames_jump_flip = []
        for i in range(sprite_sheet_jump.sheet.get_width() // 32):
            self.frames_jump_flip.append(sprite_sheet_jump.get_image(i,32,32,2,True))
        # Animação Fall
        sprite_sheet_fall = SpriteSheet(pygame.image.load("assets\Virtual Guy\Fall (32x32).png"))
        self.frame_fall = sprite_sheet_fall.get_image(0, 32, 32, 2, False)
        self.frame_fall_flip = sprite_sheet_fall.get_image(0, 32, 32, 2, True)

        self.current_frame = 0
        self.animation = "idle"
        self.animations = {
            "idle": self.frames_idle,
            "jump": self.frames_jump,
            "run": self.frames_run,
            "fall": [self.frame_fall]
            }
        self.animations_flip = {
            "idle": self.frames_idle_flip,
            "jump": self.frames_jump_flip,
            "run": self.frames_run_flip,
            "fall": [self.frame_fall_flip]
        }
        self.frames = self.animations[self.animation]
        self.texture = self.frames_idle[self.current_frame]
    def animar(self):
        # Decide qual animação usar
        if self.vel_y < 0:
            nova_animacao = "jump"
        elif self.vel_y > 0:
            nova_animacao = "fall"
        elif self.vel_x != 0:
            nova_animacao = "run"
        else:
            nova_animacao = "idle"

        # Atualiza animação apenas se mudou
        if nova_animacao != self.animation:
            self.animation = nova_animacao
            self.current_frame = 0 
        if self.flip:
            self.frames = self.animations_flip[self.animation]
        else:
            self.frames = self.animations[self.animation]

    def atualizar_frame(self, dt):
        self.current_frame += dt * 0.01
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.texture = self.frames[int(self.current_frame)]

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
            # Ajuste para evitar grudar em paredes/blocos
            if abs(self.rect.right - bloco.rect.left) < 5:  # Se estiver muito perto à direita
                self.rect.right = bloco.rect.left - 1
            elif abs(self.rect.left - bloco.rect.right) < 5:  # Se estiver muito perto à esquerda
                self.rect.left = bloco.rect.right + 1