import pygame
import map
import random


class Player(pygame.sprite.Sprite):
    # we put this here so the inventory doesn't need to call superclass init method, therefore the parameters for init
    # arent messed up

    def __init__(self, position, sprite_group, obstacle_sprites):
        super().__init__(sprite_group)
        self.inventory = Inventory()
        self.clock = pygame.time.Clock()
        self.player_hitpoints = 100
        self.armor_value = 0
        self.sprite_right = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.sprite_right_walk = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.sprite_right_walk_2 = pygame.image.load("sprites\\player\\right\\right_1.png")
        self.sprite_left = pygame.image.load("pacman-left.gif")
        self.sprite_left_walk = pygame.image.load("sprites\\player\\left\\left_0.png")
        self.sprite_left_walk_2 = pygame.image.load("sprites\\player\\left\\left_1.png")
        self.sprite_up =  pygame.image.load("pacman-up.gif")
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

    def keyboard_input(self):
        mouse_clicked = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_direction = -1
            if self.animation_num == 0:
                self.image = self.sprite_left_walk
            else:
                self.image = self.sprite_left_walk_2
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500
        elif keys[pygame.K_d]:
            self.x_direction = 1
            if self.animation_num == 0:
                self.image = self.sprite_right_walk
            else:
                self.image = self.sprite_right_walk_2
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)
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
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)
            if self.move_timer >= 500:
                self.animation_num = not self.animation_num
                self.move_timer -= 500

        elif keys[pygame.K_s]:
            self.y_direction = 1
            if self.animation_num == 0:
                self.image = self.sprite_down_walk

            else:
                self.image = self.sprite_down_walk_2
                self.walking_sounds_outdoors[random.randint(0, 3)].play()
            self.move_timer += 17  # 17*60 = about 1 second (1000)

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
            pass
        if keys[pygame.K_1]:
            pass
        if not mouse_clicked:
            if pygame.mouse.get_pressed()[0]:
                mouse_clicked = True
                print(mouse_clicked)
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)

            # change this to actually shooting the gun

            # also checks location of mouse cursor to see if there's a collision or not between a chest sprite

            # temp copied code
            # get a list of all sprites that are under the mouse cursor
            # clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]
            # do something with the clicked sprites...

            # this part  checks for whether they clicked over the inventory area


                if mouse_pos[1] in range (600,695):
                    if mouse_pos[0] in range(245,340):
                        print("success")
                    if mouse_pos[0] in range(340,435):
                        print("success2")
                    if mouse_pos[0] in range(435,530):
                        print("success3")
                    if mouse_pos[0] in range(530,625):
                        print('success4')
                    if mouse_pos[0] in range(625,720):
                        print('success5')
                    if mouse_pos[0] in range(720,815):
                        print('success6')
        if pygame.MOUSEBUTTONUP:
            mouse_clicked = False
        else:
            pass

        # code doesnt work since it still constantly plays as the animation is checked every 60 seconds so it needs to work on tick system

    def collisions(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.x_direction > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.x_direction < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.y_direction > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.y_direction < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.keyboard_input()
        self.hitbox.x += self.x_direction
        self.collisions("horizontal")
        self.hitbox.y += self.y_direction
        self.collisions("vertical")
        self.rect.center = self.hitbox.center

    def print_crosshair(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_center_x = cursor_pos[0] - 11
        cursor_center_y = cursor_pos[1] - 11
        # could movev this somewhere els to make it more efficient
        pygame.mouse.set_visible(False)
        return cursor_center_x, cursor_center_y

class Inventory(Player):
    def __init__(self):
        self.player_items = [Apple(), None, None, None, None, None]
        # hopefully the inventory won't keep resetting
        self.inventory_sprite = pygame.transform.scale(pygame.image.load("sprites\\item_sprites\\inventory_back.png"),(80,80))
        # BIG CHANGE: CHANGE INVENTORY STATE TO CLEAR ITEMS. ALSO MAKE THIS A LIST OF CLASSES (BASED ON ITEM), AND TO GET THE INFORMATION FOR THEM, USE A STR FUNCTION
        self.weapon = None
    def add_inventory_item(self, item):
        for inventory_slot in self.player_items:
            if self.player_items[inventory_slot] is None:
                # item should be a class
                self.player_items[inventory_slot] = item

    def remove_inventory_item(self, item_pos):
        self.player_items[item_pos] = None

    def use_inventory_item(self, item_pos, item_type):
        # item_type should be a 2 item list with the firt one being the general type, and the second being specific value
        if item_type[0] == "heal":
            self.player_hitpoints += item_type[1]
            if self.player_hitpoints > 100:
                self.player_hitpoints = 100
            self.remove_inventory_item(item_pos)
            # remove inventory item
        elif item_type[0] == "armor":
            self.armor_value += item_type[1]
            if self.armor_value > self.item_type[1]:
                self.armor_value = self.item_type[1]
            self.remove_inventory_item(item_pos)
        elif item_type[0] == "gun":
            # craate gun class now
            # should not remove inventory
            self.weapon = None # Gun(item_type[1])

        else:

            # you can't equip a gun if youve already ohvered over it
            # actually we can just blit the thing onto the inventory
            pass
            # play sound effect error sound maybe

        # I KINDA USE CHATGPT SO THIS AInt GONNA WORK
    def render_inventory(self, screen):
        inventory_slot_width = 50
        inventory_slot_height = 50
        inventory_margin = 10
        inventory_x = 150
        for i in range(6):
            inventory_x += 95
            screen.blit(self.inventory_sprite, (inventory_x, 600))
        inventory_x = 253
        for item in self.player_items:
            if item is not None:

                # last list should just be a sublist of all the sprites
                # THIS SHOULD BE THE SYSTEM (FIX USE INVENTORY ITEMS TOO) (item type, value of HP/consumable,(sublist of all the sprites that are associated))
                inventory_image = pygame.image.load(item.get_item_info()[2][1])
                screen.blit(inventory_image, (inventory_x,607))
            inventory_x += 95

         #   slot_x = inventory_x + i * (inventory_slot_width + inventory_margin)
          #  slot_y = inventory_y
#
 #           pygame.draw.rect(screen, (255, 255, 255), (slot_x, slot_y, inventory_slot_width, inventory_slot_height))
  #          if item is not None:
   #             # Draw the item image or text representation on the inventory slot
    #            item_image = pygame.image.load(item.image_path)  # Assuming each item has an image_path attribute
     #           screen.blit(item_image, (slot_x, slot_y))


# honestly this is kind of redundant
class Item(Player):
    def __init__(self, item_type, item_subtype, item_images, inventory_image):
        self.item_info = [item_type, item_subtype, [item_images, inventory_image]]

    def get_item_info(self):
        return self.item_info

    def display_item(self):
        # should take the image that should be displayed as a parameter, as well as coordinates for where
        pass


class Keycard(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "keycard"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class PlasticFork(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "fork"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class CanOfBeans(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "can"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Notebook(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "notebook"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class LightArmor(Item):
    def __init__(self):
        item_type = "armor"
        item_subtype = 50
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class HeavyArmor(Item):
    def __init__(self):
        item_type = "armor"
        item_subtype = 100
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class MRE(Item):
    def __init__(self):
        item_type = "heal"
        item_subtype = 75
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Water(Item):
    def __init__(self):
        item_type = "heal"
        item_subtype = 35
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Milk(Item):
    def __init__(self):
        item_type = "heal"
        item_subtype = 50
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Bandage(Item):
    def __init__(self):
        item_type = "heal"
        item_subtype = 100
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Apple(Item):
    def __init__(self):
        item_type = "heal"
        item_subtype = 20
        item_image = "sprites\\item_sprites\\apple.png"
        inventory_image = "sprites\\item_sprites\\apple_inventory.png"
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Photograph(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "photograph"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Soap(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "soap"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)


class Toothpaste(Item):
    def __init__(self):
        item_type = "other"
        item_subtype = "toothpaste"
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)

    class Gun(Player):
        def __init__(self, gun_type):
            self.gun_type = gun_type
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
            self.reload_times = {"sniper": 5, "assault_rifle": 3}
            self.gun_idle = gun_types.get(self.gun_type, {}).get("gun_idle")
            self.gun_firing = gun_types.get(self.gun_type, {}).get("gun_firing")
            self.gun_reloading = gun_types.get(self.gun_type, {}).get("gun_reloading")

        def shoot(self):
            if gun_type == "test":
                self.image = self.gun_firing

        def reload(self):
            self.image = self.gun_reloading