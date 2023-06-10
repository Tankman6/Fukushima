import pygame, map, tile, player, os, sys

from pytmx.util_pygame import load_pygame

from settings import *

os.chdir(os.getcwd())


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)


class Sprites:
    def __init__(self, screen):
        # visible sprites = seen ones that don't have collision, obstacles = collisions
        self.player = None
        self.screen = screen
        self.sprite_group = pygame.sprite.Group()
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # set up sprites and create map
        self.create_map()

    def create_map(self):
        # Initialize tmx data
        tmx_data = load_pygame('./data/tmx/fuki4.tmx')
        # cycle through layers in tmx file

        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * 32, y * 32)
                    Tile(position=pos, surface=surf, groups=self.sprite_group)

        self.player = player.Player((32, 32), [self.visible_sprites], self.obstacle_sprites)

    def update(self):
        self.sprite_group.draw(self.screen)
        self.visible_sprites.custom_draw(self.player.rect.centerx, self.player.rect.centery)
        self.visible_sprites.update()
        # update and draw the game
    # sprite_interactions


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # self.display_surface = pygame.display.get_surface()
        # self.offset = pygame.math.Vector2()

        self.cursor_image = pygame.image.load("./graphics/sprites/UI/Crosshairs_Red.png")
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2
        self.offset = [0, 0]
        self.background = pygame.image.load(os.path.join("./graphics", "map_bg.png"))
        self.background_rect = self.background.get_rect()

    def custom_draw(self, player_rect_centerx, player_rect_centery):
        self.offset[0] = player_rect_centerx - self.half_width
        self.offset[1] = player_rect_centery - self.half_height
        self.background_offset_x = self.background_rect.topleft[0] - self.offset[0]
        self.background_offset_y = self.background_rect.topleft[1] - self.offset[1]
        self.screen.blit(self.background, (self.background_offset_x, self.background_offset_y))
        for sprite in self.sprites():
            offset_x = sprite.rect.topleft[0] - self.offset[0]
            offset_y = sprite.rect.topleft[1] - self.offset[1]
            offset_pos = (offset_x, offset_y)
            self.screen.blit(sprite.image, offset_pos)
        self.screen.blit(self.cursor_image, player.Player.print_crosshair(self))
