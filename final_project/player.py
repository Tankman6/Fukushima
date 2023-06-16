import os
import pygame
from settings import *

os.chdir(os.getcwd())


def import_folder(path):
    surface_list = []

    for _, __, img_files in os.walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


class Player(pygame.sprite.Sprite):
    def __init__(self, position, sprite_group, obstacle_sprites):
        super().__init__(sprite_group)

        self.player_animations = None
        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        # General stuff
        self.image = self.player_animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        self.z = LAYERS['main']

        self.clock = pygame.time.Clock()
        self.player_hitpoints = 100
        self.armor_value = 0

        self.walking_sounds_outdoors = [pygame.mixer.Sound("./audio/footstep-outdoors-1.mp3"),
                                        pygame.mixer.Sound("./audio/footstep-outdoors-2.mp3"),
                                        pygame.mixer.Sound("./audio/footstep-outdoors-3.mp3"),
                                        pygame.mixer.Sound("./audio/footstep-outdoors-4.mp3")]

        # Movement
        self.move_timer = 0
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # Collision
        self.obstacle_sprites = obstacle_sprites

        # new method I found online to change the hitbox so that its smaller
        self.hitbox = self.rect.inflate(-5, -5)

    def import_assets(self):
        self.player_animations = {'up': [], 'down': [], 'right': [], 'left': [],
                                  'up_idle': [], 'down_idle': [], 'right_idle': [], 'left_idle': [],
                                  'up_attack': [], 'down_attack': [], 'right_attack': [], 'left_attack': []}

        for animation in self.player_animations.keys():
            full_path = "./graphics/other_player/" + animation
            self.player_animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.player_animations[self.status]):
            self.frame_index = 0

        self.image = self.player_animations[self.status][int(self.frame_index)]

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x = -5
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 5
            self.status = 'right'
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -5
            self.status = 'up'

        elif keys[pygame.K_s]:
            self.direction.y = 5
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_TAB]:
            pass
        if keys[pygame.K_1]:
            pass
        if pygame.mouse.get_pressed()[0]:
            # change this to actually shooting the gun
            if (self.direction.magnitude() == 0) and (self.status != 'attack'):
                self.status = self.status.split('_')[0] + '_attack'
        else:
            pass

    def collisions(self, direction):
        for sprite in self.obstacle_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == "horizontal":
                        # moving right
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        # moving left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
                    if direction == "vertical":
                        # moving down
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        # moving up
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def get_status(self):
        # when player is not moving
        if (self.direction.magnitude() == 0) and ('attack' not in self.status):
            self.status = self.status.split('_')[0] + '_idle'

    def move(self, dt):
        # Make sure vector direction is always 1
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collisions('horizontal')

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.keyboard_input()
        self.get_status()

        self.move(dt)
        self.animate(dt)

        # self.hitbox.x += self.x_direction
        # # self.collisions("horizontal")
        # self.hitbox.y += self.y_direction
        # # self.collisions("vertical")
        # self.rect.center = self.hitbox.center

    def print_crosshair(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_center_x = cursor_pos[0] - 11
        cursor_center_y = cursor_pos[1] - 11
        # could movev this somewhere els to make it more efficient
        pygame.mouse.set_visible(False)
        return cursor_center_x, cursor_center_y


class Inventory(Player):
    def __init__(self, screen):
        # hopefully the inventory won't keep resetting
        self.screen = screen
        self.inventory_state = [None, None, None, None, None, None]

    def add_inventory_item(self, item_pos, item):
        for inventory_slot in len(self.inventory_state):
            if self.inventory_state[inventory_slot] is None:
                self.inventory_state[inventory_slot] = item

    def remove_inventory_item(self, item_pos):
        self.inventory_state[item_pos] = None

    def use_inventory_item(self, item_pos, item_type):
        """
        item_type should be a 2 item list with the firt one being the general type, and the second being specific value
        """

        if item_type[0] == "heal":
            self.player_hitpoints += item_type[1]
            if self.player_hitpoints > 100:
                self.player_hitpoints = 100
            # remove inventory item
        elif item_type[0] == "armor":
            self.armor_value += item_type[1]
        else:
            pass
            # play sound effect error sound maybe

    def render_inventory(self):
        inventory_slot_width = 50
        inventory_slot_height = 50
        inventory_margin = 10
        inventory_x = 10
        inventory_y = 10

        for i, item in enumerate(self.inventory_state):
            slot_x = inventory_x + i * (inventory_slot_width + inventory_margin)
            slot_y = inventory_y

            pygame.draw.rect(self.screen, (255, 255, 255),
                             (slot_x, slot_y, inventory_slot_width, inventory_slot_height))
            if item is not None:
                # Draw the item image or text representation on the inventory slot
                item_image = pygame.image.load(item.image_path)  # Assuming each item has an image_path attribute
                self.screen.blit(item_image, (slot_x, slot_y))


class Gun(Player):
    def __init__(self, gun_type):
        gun_types = {
            "sniper": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_firing": None,
                "gun_reloading": None
            },
            "rifle": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png",
                "gun_firing": None,
                "gun_reloading": None
            },
            "pistol": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "gun_firing": None,
                "gun_reloading": None
            },
            "shotgun": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "gun_firing": None,
                "gun_reloading": None
            }
        }

        self.gun_idle = gun_types.get(gun_type, {}).get("gun_idle")
        self.gun_firing = gun_types.get(gun_type, {}).get("gun_firing")
        self.gun_reloading = gun_types.get(gun_type, {}).get("gun_reloading")

    def shoot(self):
        self.image = self.gun_firing


class Item(Player):
    def keycard(self):
        pass

    def money_bag(self):
        pass

    def can_of_beans(self):
        pass

    def notebook(self):
        pass

    def light_armor(self):
        pass

    def heavy_armor(self):
        pass

    def MRE(self):
        pass

    def water(self):
        pass

    def milk(self):
        pass

    def bandage(self):
        pass

    def iPod(self):
        pass

    def photograph(self):
        pass

    def soap(self):
        pass

    def toothpaste(self):
        pass
