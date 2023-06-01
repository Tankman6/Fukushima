import pygame
import map


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, sprite_group):
        super().__init__(sprite_group)
        self.image = pygame.image.load("03.png")
        print("HIDSFHUISDFHUSDIF")
        self.rect = self.image.get_rect(topleft=position)
        # new method i found online to change the hitbox so that its smaller
        # if tile type = (something) change the hitbox accordingly, this one is currently for the tree
        self.hitbox = self.rect.inflate(-100,-50)
