import pygame
import map
import random
import sprites

class Player(pygame.sprite.Sprite):
    # we put this here so the inventory doesn't need to call superclass init method, therefore the parameters for init
    # arent messed up

    def __init__(self, position, sprite_group, obstacle_sprites, screen):
        super().__init__(sprite_group)
        self.screen = screen
        self.mouse_clicked = False
        self.clock = pygame.time.Clock()
        self.player_hitpoints = 100
        self.armor_value = 100
        self.inventory = Inventory(self.player_hitpoints, self.armor_value, self.screen)
        self.sprite_right = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.sprite_right_walk = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.sprite_right_walk_2 = pygame.image.load("sprites\\player\\right\\right_1.png")
        self.sprite_left = pygame.image.load("sprites\\player\\left\\left_0.png")
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
        self.pain_sounds = [pygame.mixer.Sound("audio\\pain_sound.wav"),pygame.mixer.Sound("audio\\pain_sound_2.wav"), pygame.mixer.Sound("audio\\pain_sound_3.wav")]
        self.death_sounds = [pygame.mixer.Sound("audio\\death_sound.wav"), pygame.mixer.Sound("audio\\death_sound_2.wav"), pygame.mixer.Sound("audio\\death_sound_3.wav")]
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
        self.reload_pressed = None

    def keyboard_input(self, bullet_sprites):
        keys = pygame.key.get_pressed()
        if self.inventory.weapon is not None:
            self.image = self.sprite_right_walk_2
        if keys[pygame.K_a]:
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
        elif keys[pygame.K_d]:
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

        if keys[pygame.K_w]:
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

        elif keys[pygame.K_s]:
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
        if keys[pygame.K_r]:
            if self.inventory.weapon is not None:
                self.reload_pressed = True
                self.gun_reloading_sound = pygame.mixer.Sound("audio\\gun_reload.mp3")
                channel3 = pygame.mixer.Channel(2)
                channel3.play(self.gun_reloading_sound)

        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(6):
                if mouse_pos[0] in range(245 + 95 * i, 340 + 95 * i):
                    if mouse_pos[1] in range(600, 695):
                        if self.inventory.player_items[i] is not None and not self.mouse_clicked:
                            print('hi')
                            if self.inventory.player_items[i].get_item_info()[0] == "gun" and self.inventory.weapon is not None:
                                self.inventory.weapon = None
                                print("STOP DISPLAYING GUN")
                                continue
                            self.inventory.use_inventory_item(i, self.inventory.player_items[i].get_item_info())

                            self.animation_num = 1
            # Mouse cursor is not over the inventory area
            if self.inventory.weapon is not None and (not (245 <= mouse_pos[0] <= 720 and 600 <= mouse_pos[1] <= 695)):
                if self.mouse_clicked is False:
                    self.inventory.weapon.shoot(self.screen,mouse_pos, bullet_sprites, self.obstacle_sprites, self.rect)

            # Set mouse clicked to True
            self.mouse_clicked = True
        else:
            # Mouse button is not pressed
            # Reset mouse clicked to False
            self.mouse_clicked = False
            # for if you click menu button
        if pygame.mouse.get_pressed()[2]:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(6):
                if mouse_pos[0] in range(245 + 95 * i, 340 + 95 * i):
                    if mouse_pos[1] in range(600, 695):
                        if self.inventory.player_items[i] is not None:
                            self.inventory.remove_inventory_item(i)


        # code doesnt work since it still constantly plays as the animation is checked every 60 seconds so it needs to work on tick system
    def collisions(self, direction, bullet_sprites):
        # this doesn't work unless if a bullet hits yourself
        for sprite in bullet_sprites:
            if sprite.rect.colliderect(self.rect):
                channel5 = pygame.mixer.Channel(4)
                channel5.play(self.pain_sounds[random.randint(0,2)])
                if self.inventory.armor_value == 0:
                    self.inventory.player_hitpoints -= sprite.bullet_damage
                else:
                    self.inventory.armor_value -= sprite.bullet_damage
                    if self.inventory.armor_value < 0:
                        self.inventory.player_hitpoints += self.inventory.armor_value
                        self.inventory.armor_value = 0
                sprite.kill()
                print("WOW IT HAPPENED")

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.x_direction > 0:  # moving right
                        self.rect.right = sprite.rect.left
                    if self.x_direction < 0:  # moving left
                        self.rect.left = sprite.rect.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.y_direction > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.y_direction < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self, bullet_sprites, player_position, bot_group):
        if self.inventory.player_hitpoints <= 0:
            channel6 = pygame.mixer.Channel(5)
            channel6.play(self.death_sounds[random.randint(0, 2)])
            self.kill()

        self.keyboard_input(bullet_sprites)

        if self.inventory.weapon and self.reload_pressed is not None:
            if self.inventory.weapon.bullet_capacity != self.inventory.weapon.max_bullet_capacity:
                self.inventory.weapon.reload()
            else:
                self.reload_pressed = None

        self.rect.x += self.x_direction
        self.rect.y += self.y_direction


        self.collisions("horizontal", bullet_sprites)
        self.collisions("vertical", bullet_sprites)

        self.inventory.render_player_items(self.rect)


    def print_crosshair(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_center_x = cursor_pos[0] - 11
        cursor_center_y = cursor_pos[1] - 11
        # could movev this somewhere els to make        it more efficient

        return cursor_center_x, cursor_center_y

class Inventory(Player):
    def __init__(self, player_hitpoints, armor_value, screen):
        self.screen = screen
        self.player_hitpoints = player_hitpoints
        self.hp_bars = pygame.transform.scale(pygame.image.load("sprites\\UI_sprites\\health_bar.png"), (333, 45))
        self.hp_bars_bg = pygame.Surface((333, 45))
        self.hp_bars_bg.fill((64, 64, 64))
        self.armor_value = armor_value
        self.player_items = [Apple(), Gun("shotgun"), Gun("rifle"), Gun("pistol"), Gun("sniper"), Gun("shotgun")]
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
            self.weapon = self.player_items[item_pos]

        else:

            # you can't equip a gun if youve already ohvered over it
            # actually we can just blit the thing onto the inventory
            pass
            # play sound effect error sound maybe
    def unequip_gun(self):
        self.weapon = None
    def render_player_items(self, player_rect):
        inventory_slot_width = 50
        inventory_slot_height = 50
        inventory_margin = 10
        inventory_x = 150
        for i in range(6):
            inventory_x += 95
            self.screen.blit(self.inventory_sprite, (inventory_x, 600))
        inventory_x = 253
        for item in self.player_items:
            if item is not None:

                # last list should just be a sublist of all the sprites
                # THIS SHOULD BE THE SYSTEM (FIX USE INVENTORY ITEMS TOO) (item type, value of HP/consumable,(sublist of all the sprites that are associated))
                inventory_image = pygame.image.load(item.get_item_info()[2][1])
                self.screen.blit(inventory_image, (inventory_x,607))
            inventory_x += 95
        # now we render the gun
        if self.weapon is not None:
            self.weapon.display_gun(self.screen, player_rect)
            # change image here?
        # now we render the HP bars and everything]
        # calculate armor and HP bar

        # Calculate the length of the health and armor bars based on player's hit points
        health_length = int((self.player_hitpoints / 100) * 333)
        armor_length = int((self.armor_value / 100) * 333)


        # Create the health value and armor bar based on the calculated lengths
        if health_length > 0:
            health_value_bar = pygame.Surface((health_length, 22))
        else:
            health_value_bar = pygame.Surface((0, 22))
        health_value_bar.fill((0, 255, 0))  # Green color

        armor_value_bar = pygame.Surface((armor_length, 22))
        armor_value_bar.fill((70, 130, 180))  # Cyan color

        # Render the health and armor bars on the screen

        self.screen.blit(self.hp_bars_bg,(356,550))
        self.screen.blit(health_value_bar, (356, 550))
        self.screen.blit(armor_value_bar, (356, 550 + 22))
        self.screen.blit(self.hp_bars, (356, 550))

# honestly this is kind of redundant
class Item(Player):
    def __init__(self, item_type, item_subtype, item_images, inventory_image):
        self.item_info = [item_type, item_subtype, [item_images, inventory_image]]

    def get_item_info(self):
        return self.item_info

class Armor(Item):
    def __init__(self):
        item_type = "armor"
        item_subtype = 50
        item_image = None
        inventory_image = None  # [/* inventory image directory here */]
        super().__init__(item_type, item_subtype, item_image, inventory_image)

class Apple(Item):
    def __init__(self):
        item_type = "heal"
        item_subtype = 35
        item_image = "sprites\\item_sprites\\apple.png"
        inventory_image = "sprites\\item_sprites\\apple_inventory.png"
        super().__init__(item_type, item_subtype, item_image, inventory_image)

class Gun(Item):
    def __init__(self, gun_type):
        self.item_type = "gun"
        self.gun_type = gun_type
        gun_types = {
            "sniper": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\sniper_inventory.png",
                "bullet_capacity": 1,
                "bullet_damage": 150,
                "reload_time": 180
            },
            "rifle": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\assault_rifle_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\assault_rifle_inventory.png",
                "bullet_capacity": 30,
                "bullet_damage": 28,
                "reload_time": 180
            },
            "pistol": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\pistol_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\pistol_inventory.png",
                "bullet_capacity": 15,
                "bullet_damage": 15,
                "reload_time": 120
            },
            "shotgun": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\shotgun_idle.png",
                "inventory_image": "sprites\\gun_sprites\\PNG\\shotgun_inventory.png",
                "bullet_capacity": 6,
                "bullet_damage": 25,
                "reload_time": 180
            }
        }
        self.gun_idle = gun_types.get(self.gun_type, {}).get("gun_idle")
        self.gun_firing = gun_types.get(self.gun_type, {}).get("gun_firing")
        self.gun_firing_sound = pygame.mixer.Sound("audio\\gun_firing.mp3")
        self.gun_reloading = gun_types.get(self.gun_type, {}).get("gun_reloading")
        self.gun_inventory = gun_types.get(self.gun_type, {}).get("inventory_image")
        # if gun_bullets is not None: self.bullet_capacity = gun_bullets
        self.max_bullet_capacity = self.bullet_capacity = gun_types.get(self.gun_type, {}).get("bullet_capacity")
        self.bullet_damage = gun_types.get(self.gun_type, {}).get("bullet_damage")
        self.reload_time = gun_types.get(self.gun_type, {}).get("reload_time")
        self.gun_font = pygame.font.SysFont("arial", 35)
        self.bullet_capacity_text = self.gun_font.render(str(self.bullet_capacity), True, (255,255,255))
        self.reload_start_time = 0
        super().__init__(self.item_type, self.gun_type, [self.gun_idle, self.gun_firing, self.gun_reloading], self.gun_inventory)

    def display_gun(self, screen, player_pos):
        gun_name_text = self.gun_font.render(self.gun_type, True, (255,255,255))
        bullet_count_text = self.gun_font.render(str(self.bullet_capacity), True, (255,255,255))
        forward_slash = self.gun_font.render("/", True, (255, 255, 255))
        gun_idle_png = pygame.image.load(self.gun_idle)
        screen.blit(gun_idle_png, (player_pos[0]+50,player_pos[1]+15))
        screen.blit(gun_name_text, (50, 550))
        screen.blit(bullet_count_text, (35,590))
        screen.blit(forward_slash, (67,590))
        screen.blit(self.bullet_capacity_text, (75,590))

    def shoot(self, screen, mouse_position, bullet_sprite_group, obstacle_sprites, player_pos):
        if self.bullet_capacity > 0:
            channel2 = pygame.mixer.Channel(1)
            channel2.play(self.gun_firing_sound)
            self.bullet_capacity -= 1

            gun_firing_png = pygame.image.load(self.gun_firing)
            screen.blit(gun_firing_png,(player_pos[0]+50,player_pos[1]+15))
            print("hi")
            if self.gun_type == "shotgun":
                for i in range(3):
                    if i == 0:  # Deviated bullets for spread effect
                        deviation = 75
                          # Deviation for y-component
                        bullet_direction = pygame.Vector2(mouse_position[0] - player_pos[0] + deviation,
                                                          mouse_position[1] - player_pos[1] + deviation)
                        bullet = Bullet(mouse_position, gun_firing_png, obstacle_sprites, screen, bullet_direction, player_pos, self.bullet_damage)
                    elif i == 2:
                        deviation = 45  # Deviation for x-component
                        # Deviation for y-component
                        bullet_direction = pygame.Vector2(mouse_position[0] - player_pos[0] - deviation,
                                                          mouse_position[1] - player_pos[1] - deviation)
                        bullet = Bullet(mouse_position, gun_firing_png, obstacle_sprites, screen, bullet_direction, player_pos, self.bullet_damage)
                    else:  # Center bullet, no deviation
                        bullet = Bullet(mouse_position, gun_firing_png, obstacle_sprites, screen, None, player_pos, self.bullet_damage)
                    bullet_sprite_group.add(bullet)
                    bullet.update()
            else:
                bullet = Bullet(mouse_position, gun_firing_png, obstacle_sprites, screen, None, player_pos, self.bullet_damage)
                bullet_sprite_group.add(bullet)
                bullet.update()


        # make group of bullet sprites here
        # bullet.go(vector_direction)

    def reload(self):
        self.reload_start_time += 1
        print(self.reload_start_time)
        self.image = self.gun_reloading
        # Make sure that they can't shoot if this is the case
        self.bullet_capacity = 0  # Set bullet capacity to 0 during reload
        if self.reload_start_time >= self.reload_time:
            self.bullet_capacity = self.max_bullet_capacity  # Refill the magazine after reload
            self.image = self.gun_idle
            self.reload_start_time = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, mouse_position, gun_image, obstacle_sprites, screen, custom_direction, player_rect, damage):
        super().__init__()
        self.bullet_damage = damage
        self.screen = screen
        self.obstacle_sprites = obstacle_sprites
        self.image = pygame.Surface([12, 6])
        self.image.fill((255, 204, 0))
        self.rect = self.image.get_rect()
        self.player_rect = player_rect
        self.rect.center = (self.player_rect[0] + gun_image.get_width() + 50, self.player_rect.y + 28)
        if custom_direction is None:
            direction = pygame.math.Vector2(mouse_position[0] - self.player_rect.x, mouse_position[1] - self.rect[1])
        else:
            direction = custom_direction
        self.direction = direction.normalize()  # Normalize the direction vector

    def update(self):
        speed = 7.0  # Adjust this value to control the bullet's speed
        self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self.rect.y += self.direction.y * speed

        if self.rect.centerx < 0 or self.rect.centerx > 1080 or self.rect.centery < 0 or self.rect.centery > 720:
            self.kill()
