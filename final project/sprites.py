import pygame, map, tile, player


class Sprites:
    def __init__(self, screen):
        # visible sprites = seen ones that don't have collision, obstacles = collisions
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        # set up sprites and create map
        self.create_map()

    def create_map(self):
        # layer num allows certain sprites to be generated lower/higher than others
        for layer_num in range(2):
            for row in range(len(map.Fukushima_Map)):
                for col in range(len(map.Fukushima_Map[row])):
                    x_pos = col * map.TILESIZE
                    y_pos = row * map.TILESIZE
                    # HERE WE SHOULD FIX WHAT SPRITES SHOULD BE LOWER/HIGHER THAN THE PLAYER. Otherwise though it doesn't mater
                    if map.Fukushima_Map[row][col] == "P":
                        if layer_num == 0:
                            self.player = player.Player((x_pos, y_pos), [self.visible_sprites], self.obstacle_sprites)
                    if map.Fukushima_Map[row][col] == "O":
                        if layer_num == 1:
                            tile.Tile((x_pos, y_pos), [self.visible_sprites, self.obstacle_sprites])

    def update(self):
        self.visible_sprites.custom_draw(self.player.rect.centerx, self.player.rect.centery)
        self.visible_sprites.update()
        # update and draw the game
    # sprite_interactions


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.cursor_image = pygame.image.load("sprites\\Crosshairs_Red.png")
        self.screen = pygame.display.get_surface()
        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2
        self.offset = [0, 0]
        self.background = pygame.image.load("ground.png")
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
        self.screen.blit(self.cursor_image, player.Weapon.print_crosshair(self))
