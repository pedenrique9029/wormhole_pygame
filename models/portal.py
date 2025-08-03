import pygame
from models.body import Body
from models.spritesheet import SpriteSheet


class Portal(Body):
    def __init__(self, texture, x, y, colisores):
        super().__init__(texture, x, y, 64, 64, colisores,True)
        # Carrega o spritesheet do portal
        sprite_sheet_portal = SpriteSheet(pygame.image.load("assets\portal.png"))
        # Animação do portal
        self.frames_spinning = []
        for i in range(sprite_sheet_portal.sheet.get_width() // 32):
            self.frames_spinning.append(sprite_sheet_portal.get_image(i, 32, 32, 3, False))
        self.current_frame = 0

    def animar(self):
        # Atualiza a animação do portal
        self.current_frame += 0.15
        if self.current_frame >= len(self.frames_spinning):
            self.current_frame = 0
        self.texture = self.frames_spinning[int(self.current_frame)]