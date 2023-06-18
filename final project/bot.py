import pygame
import map
import random


class Bot(pygame.sprite.Sprite):
    # we put this here so the inventory doesn't need to call superclass init method, therefore the parameters for init
    # arent messed up

    # we put this here so the inventory doesn't need to call superclass init method, therefore the parameters for init
    # arent messed up

    def __init__(self, position, sprite_group, obstacle_sprites, screen):
        super().__init__(sprite_group)
        self.bullet_sprites = pygame.sprite.Group()
        self.screen = screen
        self.mouse_clicked = False
        self.clock = pygame.time.Clock()
        self.player_hitpoints = 100
        self.armor_value = 0
        self.inventory = Inventory(self.player_hitpoints, self.armor_value, self.screen)
        self.sprite_right = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.sprite_right_walk = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.sprite_right_walk_2 = pygame.image.load("sprites\\player\\right\\right_1.png")
        self.sprite_left = pygame.image.load("pacman-left.gif")
        self.sprite_left_walk = pygame.image.load("sprites\\player\\left\\left_0.png")
        self.sprite_left_walk_2 = pygame.image.load("sprites\\player\\left\\left_1.png")
        self.sprite_up = pygame.image.load("pacman-up.gif")
        self.sprite_up_walk = pygame.image.load("sprites\\player\\up\\up_0.png")
        self.sprite_up_walk_2 = pygame.image.load("sprites\\player\\up\\up_1.png")
        self.sprite_down = pygame.image.load("pacman-down.gif")
        self.sprite_down_walk = pygame.image.load("sprites\\player\\down\\down_0.png")
        self.sprite_down_walk_2 = pygame.image.load("sprites\\player\\down\\down_1.png")
        self.walking_sounds_outdoors = [pygame.mixer.Sound("audio\\footstep-outdoors-1.mp3"),
                                        pygame.mixer.Sound("audio\\footstep-outdoors-2.mp3"),
                                        pygame.mixer.Sound("audio\\footstep-outdoors-3.mp3"),
                                        pygame.mixer.Sound("audio\\footstep-outdoors-4.mp3")]
        # self.up_direction_sprites = [self.sprite_up_walk, self.sprite_up_walk_2]
        # self.down_direction_sprites = [self.sprite_down_walk, self.sprite_down_walk_2]
        # self.left_direction_sprites = [self.sprite_left_walk, self.sprite_left_walk_2]
        # self.right_direction_sprites = [self.sprite_right_walk, self.sprite_right_walk_2]
        self.image = self.sprite_right
        self.rect = self.image.get_rect(topleft=position)
        self.x_direction = 0
        self.y_direction = 0
        self.obstacle_sprites = obstacle_sprites
        self.move_timer = 0
        self.animation_num = 0
        # new method i found online to change the hitbox so that its smaller
        self.hitbox = self.rect.inflate(-5, -5)

        self.walking_direction = 0
        self.walking_direction_timer = 0

    def move_ai(self):
        if self.inventory.weapon is not None:
            self.image = self.sprite_right_walk_2
        if self.walking_direction == 4:
            # A KEYS DIRECTION
            self.x_direction = -1
            if self.animation_num == 0:
                self.image = self.sprite_left_walk if self.inventory.weapon is None else self.image
            else:
                self.image = self.sprite_left_walk_2 if self.inventory.weapon is None else self.image
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        elif self.walking_direction == 2:
            # D Key direction
            self.x_direction = 1
            if self.animation_num == 0:
                self.image = self.sprite_right_walk if self.inventory.weapon is None else self.image
            else:
                self.image = self.sprite_right_walk_2 if self.inventory.weapon is None else self.image
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        else:
            if self.x_direction == -1:
                self.image = self.sprite_left if self.inventory.weapon is None else self.image
            elif self.x_direction == 1:
                self.image = self.sprite_right if self.inventory.weapon is None else self.image
            self.x_direction = 0

        if self.walking_direction == 3:
            # W key direction:
            self.y_direction = -1
            if self.animation_num == 0:
                self.image = self.sprite_up_walk if self.inventory.weapon is None else self.image
            else:
                self.image = self.sprite_up_walk_2 if self.inventory.weapon is None else self.image
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500

        elif self.walking_direction == 1:
            # S key direction
            self.y_direction = 1
            if self.animation_num == 0:
                self.image = self.sprite_down_walk if self.inventory.weapon is None else self.image

            else:
                self.image = self.sprite_down_walk_2 if self.inventory.weapon is None else self.image
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)

            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        else:
            if self.y_direction == -1:
                self.image = self.sprite_up if self.inventory.weapon is None else self.image
            elif self.y_direction == 1:
                self.image = self.sprite_down if self.inventory.weapon is None else self.image
            self.y_direction = 0

        # code doesnt work since it still constantly plays as the animation is checked every 60 seconds so it needs to work on tick system

# make collision so that the player goes the opposite direction if it hits a wall
# also if a bullet hits the sprite it starts shooting
    def collisions(self, direction):
        for sprite in self.bullet_sprites:
            if sprite.rect.colliderect(self.hitbox):
                self.player_hitpoints -= 25
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.x_direction > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                        #self.walking_direction = 2
                    if self.x_direction < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                        #self.walking_direction = 4
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    print("occurred")
                    if self.y_direction > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        # self.walking_direction = 1
                    if self.y_direction < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        #self.walking_direction = 3
    def update(self):
        self.walking_direction_timer += 1


        # this changes patrol radius
        if self.walking_direction_timer % 350 == 0:
            self.walking_direction += 1
        if self.walking_direction > 4:
            self.walking_direction = 0
        self.move_ai()
        self.hitbox.x += self.x_direction
        self.collisions("horizontal")
        self.hitbox.y += self.y_direction
        self.collisions("vertical")
        self.rect.center = self.hitbox.center
        # implement this properly
        self.bullet_sprites.draw(self.screen)
        self.bullet_sprites.update()


    def print_crosshair(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_center_x = cursor_pos[0] - 11
        cursor_center_y = cursor_pos[1] - 11
        # could movev this somewhere els to make        it more efficient
        # pygame.mouse.set_visible(True)
        return cursor_center_x, cursor_center_y

# remove self.add and reomve inventory items
class Inventory(Bot):
    def __init__(self, player_hitpoints, armor_value, screen):
        self.screen = screen
        self.player_hitpoints = player_hitpoints
        self.armor_value = armor_value
        self.player_items = [Gun("pistol"), None, None, None, None]
        # hopefully the inventory won't keep resetting
        self.inventory_sprite = pygame.transform.scale(pygame.image.load("sprites\\item_sprites\\inventory_back.png"),(80,80))
        # BIG CHANGE: CHANGE INVENTORY STATE TO CLEAR ITEMS. ALSO MAKE THIS A LIST OF CLASSES (BASED ON ITEM), AND TO GET THE INFORMATION FOR THEM, USE A STR FUNCTION
        self.weapon = Gun("gun"[1])

# honestly this is kind of redundant
class Item(Bot):
    def __init__(self, item_type, item_subtype, item_images, inventory_image):
        self.item_info = [item_type, item_subtype, [item_images, inventory_image]]

class Gun(Item):
    def __init__(self, gun_type):
        self.item_type = "gun"
        self.gun_type = gun_type
        gun_types = {
            "sniper": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "inventory_image": "prites\\gun_sprites\\PNG\\sniper_inventory.png"
            },
            "rifle": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png", # fix this (change image beause it works now)
                "gun_reloading": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\assault_rifle_inventory.png"
            },
            "pistol": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\pistol_inventory.png"
            },
            "shotgun": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\shotgun_inventory.png"
            }
        }
        self.reload_times = {"sniper": 5, "assault_rifle": 3, "shotgun": 5, "pistol": 2}
        self.gun_idle = gun_types.get(self.gun_type, {}).get("gun_idle")
        self.gun_firing = gun_types.get(self.gun_type, {}).get("gun_firing")
        self.gun_reloading = gun_types.get(self.gun_type, {}).get("gun_reloading")
        self.gun_inventory = gun_types.get(self.gun_type, {}).get("inventory_image")
        super().__init__(self.item_type, self.gun_type, [self.gun_idle, self.gun_firing, self.gun_reloading], self.gun_inventory)

    def display_gun(self, screen):
        gun_idle_png = pygame.image.load(self.gun_idle)
        screen.blit(gun_idle_png, (555, 364))

    def shoot(self, screen, mouse_position, bullet_sprite_group, obstacle_sprites):

        gun_firing_png = pygame.image.load(self.gun_firing)
        screen.blit(gun_firing_png, (555, 364))

        bullet = Bullet(mouse_position, gun_firing_png, obstacle_sprites, screen)
        bullet_sprite_group.add(bullet)
        bullet.update()
        bullet.collisions()

        # make group of bullet sprites here
        # bullet.go(vector_direction)

    def reload(self):
        self.image = self.gun_reloading
        # make sure that they can't shoot if this is the case

class Bullet(pygame.sprite.Sprite):
    def __init__(self, mouse_position,gun_image, obstacle_sprites, screen):
        super().__init__()
        self.screen = screen
        self.obstacle_sprites = obstacle_sprites
        self.image = pygame.Surface([12, 6])
        self.image.fill((255,204,0))
        self.rect = self.image.get_rect()
        self.rect.center = (560+gun_image.get_width(),368)
        self.direction = pygame.math.Vector2(mouse_position[0]-560, mouse_position[1] - 350)



    # doesn't work as it detects tiles only (for the above)


    def update(self):
        self.rect.center += self.direction * 0.1
        if self.rect.centerx < 0 or self.rect.centerx > 1080 or self.rect.centery < 0 or self.rect.centery > 720:
            self.kill()
        self.collisions()
        # how


    #outline: this code should basically calculate the direction it must go, then move towards that direction at a certain speed (depends on the gun)
    #and also then when it collides (or it goes past a certain limit (maybe longest diagonal from the center to corner of screen)) it should end itself
    #then we need to blit the bullets to the screen
    #there should also be a group to go with this


    # fix the issue with adding the bullet to the bullet_sprites sprite group (probably right after yu instantiate the class)
    # then just fix how the bulltes move
    # then add reloading sfx
    # also make sure to remove bullets after a certain point
    # also make sure theyre bliting right