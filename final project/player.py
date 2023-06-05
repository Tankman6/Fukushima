import pygame
import map


class Player(pygame.sprite.Sprite):
    def __init__(self, position, sprite_group, obstacle_sprites):
        super().__init__(sprite_group)
        self.clock = pygame.time.Clock()
        self.sprite_right = pygame.image.load("pacman-right.gif")
        self.sprite_right_walk = pygame.image.load("player\\right\\right_0.png")
        self.sprite_right_walk_2 = pygame.image.load("player\\right\\right_1.png")
        self.sprite_left = pygame.image.load("pacman-left.gif")
        self.sprite_left_walk = pygame.image.load("player\\left\\left_0.png")
        self.sprite_left_walk_2 = pygame.image.load("player\\left\\left_1.png")
        self.sprite_up = pygame.image.load("pacman-up.gif")
        self.sprite_up_walk = pygame.image.load("player\\up\\up_0.png")
        self.sprite_up_walk_2 = pygame.image.load("player\\up\\up_1.png")
        self.sprite_down = pygame.image.load("pacman-down.gif")
        self.sprite_down_walk = pygame.image.load("player\\down\\down_0.png")
        self.sprite_down_walk_2 = pygame.image.load("player\\down\\down_1.png")
        self.walking_sounds_outdoors = [pygame.mixer.Sound("audio\\footstep-outdoors-1"),pygame.mixer.Sound("audio\\footstep-outdoors-2"), pygame.mixer.Sound("audio\\footstep-outdoors-3"), pygame.mixer.Sound("audio\\footstep-outdoors-4")]
        #self.up_direction_sprites = [self.sprite_up_walk, self.sprite_up_walk_2]
        #self.down_direction_sprites = [self.sprite_down_walk, self.sprite_down_walk_2]
        #self.left_direction_sprites = [self.sprite_left_walk, self.sprite_left_walk_2]
        #self.right_direction_sprites = [self.sprite_right_walk, self.sprite_right_walk_2]
        self.image = self.sprite_right
        self.rect = self.image.get_rect(topleft=position)
        self.x_direction = 0
        self.y_direction = 0
        self.obstacle_sprites = obstacle_sprites
        self.move_timer = 0
        self.animation_num = 0
        # new method i found online to change the hitbox so that its smaller
        self.hitbox = self.rect.inflate(-5, -5)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_direction = -1
            if self.animation_num == 0:
                self.image = self.sprite_left_walk
            else:
                self.image = self.sprite_left_walk_2
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            print(self.move_timer)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        elif keys[pygame.K_d]:
            self.x_direction = 1
            if self.animation_num == 0:
                self.image = self.sprite_right_walk
            else:
                self.image = self.sprite_right_walk_2
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            print(self.move_timer)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        else:
            if self.x_direction == -1:
                self.image = self.sprite_left
            elif self.x_direction == 1:
                self.image = self.sprite_right
            self.x_direction = 0

        if keys[pygame.K_w]:
            self.y_direction = -1
            if self.animation_num == 0:
                self.image = self.sprite_up_walk
            else:
                self.image = self.sprite_up_walk_2
            self.move_timer += 17 # 17*60 = about 1 second (1000)
            print(self.move_timer)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500

        elif keys[pygame.K_s]:
            self.y_direction = 1
            if self.animation_num == 0:
                self.image = self.sprite_down_walk
            else:
                self.image = self.sprite_down_walk_2
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            print(self.move_timer)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        else:
            if self.y_direction == -1:
                self.image = self.sprite_up
            elif self.y_direction == 1:
                self.image = self.sprite_down
            self.y_direction = 0

        if keys[pygame.K_TAB]:
            print("test2")
        if keys[pygame.K_1]:
            print("HI")
            


    def collisions(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.x_direction > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.x_direction < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.y_direction > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.y_direction < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def inventory(self):
        print("HI")

    def weapons(self):
        print("HI")
    def update(self):
        self.keyboard_input()
        self.hitbox.x += self.x_direction
        self.collisions("horizontal")
        self.hitbox.y += self.y_direction
        self.collisions("vertical")
        self.rect.center = self.hitbox.center
