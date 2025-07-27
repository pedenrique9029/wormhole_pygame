import pygame


class SpriteSheet:
    def __init__(self, sheet):
        self.sheet = sheet

    def get_image(self, frame, width, height, scale, flip_h):
        # Cria uma superfície temporária para extrair o frame
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(
            self.sheet,
            (0, 0),
            (frame * width, 0, width, height)  # Área do spritesheet a ser copiada
        )

        # Aplica escala e flip
        image = pygame.transform.scale(image, (width * scale, height * scale))
        if flip_h:  # Só aplica flip se necessário
            image = pygame.transform.flip(image, True, False)

        return image