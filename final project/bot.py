import pygame
import map
import random

class Bot(pygame.sprite.Sprite):
    # we put this here so the inventory doesn't need to call superclass init method, therefore the parameters for init
    # arent messed up

    def __init__(self, position, sprite_group, obstacle_sprites, screen):
        super().__init__(sprite_group)
        self.position = position
        self.bullet_sprites = pygame.sprite.Group()
        self.screen = screen
        self.mouse_clicked = False
        self.clock = pygame.time.Clock()
        self.player_hitpoints = 100
        self.armor_value = 0
        self.inventory = Inventory(self.player_hitpoints, self.armor_value)
        self.sprite_right = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.walking_sounds_outdoors = [pygame.mixer.Sound("audio\\footstep-outdoors-1.mp3"),
                                        pygame.mixer.Sound("audio\\footstep-outdoors-2.mp3"),
                                        pygame.mixer.Sound("audio\\footstep-outdoors-3.mp3"),
                                        pygame.mixer.Sound("audio\\footstep-outdoors-4.mp3")]
        self.image = self.sprite_right
        self.rect = self.image.get_rect()
        self.x_direction = 0
        self.y_direction = 0
        self.obstacle_sprites = obstacle_sprites

        # new method i found online to change the hitbox so that its smaller
        print(self.rect)
        self.hitbox = self.rect #.inflate(-5, -5)
        print(self.hitbox)
        self.reload_pressed = None
        self.walking_direction = 0
        self.walking_direction_timer = 0

    def move_ai(self):
        if self.inventory.weapon is not None:
            self.image = self.sprite_right
        if self.walking_direction == 4:
            self.x_direction = -1
        elif self.walking_direction == 2:
            self.x_direction = 1
        else:
            self.x_direction = 0

        if self.walking_direction == 3:
            self.y_direction = -1
        elif self.walking_direction == 1:
            self.y_direction = 1
        else:
            self.y_direction = 0

        # code doesnt work since it still constantly plays as the animation is checked every 60 seconds so it needs to work on tick system

    def collisions(self, direction):
        pass
        # this doesn't work unless if a bullet hits yourself
        #for bullet in main.sprites.character.bullet_sprites:
            #if bullet.rect.colliderect(self.hitbox):
                #self.player_hitpoints -= 25
                #print("Collision occurred with bullet")

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
        self.walking_direction_timer += 1
        if self.walking_direction_timer % 350 == 0:
            self.walking_direction += 1
        if self.walking_direction > 4:
            self.walking_direction = 0
        self.move_ai()
        if self.inventory.weapon:
            if self.inventory.weapon.bullet_capacity <= 0:
                self.inventory.weapon.reload()
            else:
                self.reload_pressed = None
        self.hitbox.x += self.x_direction
        self.collisions("horizontal")
        self.hitbox.y += self.y_direction
        self.collisions("vertical")
        self.rect.topleft = self.hitbox.topleft  # Update rect position to match hitbox
        self.bullet_sprites.draw(self.screen)
        self.bullet_sprites.update()
        self.inventory.weapon.display_gun(self.screen, self.hitbox)


    def print_crosshair(self):
        cursor_pos = pygame.mouse.get_pos()
        cursor_center_x = cursor_pos[0] - 11
        cursor_center_y = cursor_pos[1] - 11
        # could movev this somewhere els to make        it more efficient

        return cursor_center_x, cursor_center_y

class Inventory(Bot):
    def __init__(self, player_hitpoints, armor_value):
        self.player_hitpoints = player_hitpoints
        self.armor_value = armor_value
        # BIG CHANGE: CHANGE INVENTORY STATE TO CLEAR ITEMS. ALSO MAKE THIS A LIST OF CLASSES (BASED ON ITEM), AND TO GET THE INFORMATION FOR THEM, USE A STR FUNCTION
        self.weapon = Gun("rifle")
            # change image here?


# honestly this is kind of redundant
class Item(Bot):
    def __init__(self, item_type, item_subtype, item_images, inventory_image):
        self.item_info = [item_type, item_subtype, [item_images, inventory_image]]

    def get_item_info(self):
        return self.item_info

class Gun(Item):
    def __init__(self, gun_type):
        self.item_type = "gun"
        self.gun_type = gun_type
        gun_types = {
            "sniper": {
                "gun_idle": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_firing": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "gun_reloading": "sprites\\gun_sprites\\PNG\\sniper_rifle_idle.png",
                "inventory_image": "prites\\gun_sprites\\PNG\\sniper_inventory.png",
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
                "reload_time": 300
            }
        }
        self.gun_idle = gun_types.get(self.gun_type, {}).get("gun_idle")
        self.gun_firing = gun_types.get(self.gun_type, {}).get("gun_firing")
        self.gun_reloading = gun_types.get(self.gun_type, {}).get("gun_reloading")
        self.gun_inventory = gun_types.get(self.gun_type, {}).get("inventory_image")
        # if gun_bullets is not None: self.bullet_capacity = gun_bullets
        self.max_bullet_capacity = self.bullet_capacity = gun_types.get(self.gun_type, {}).get("bullet_capacity")
        self.bullet_damage = gun_types.get(self.gun_type, {}).get("bullet_damage")
        self.reload_time = gun_types.get(self.gun_type, {}).get("reload_time")
        self.gun_font = pygame.font.SysFont("arial", 35)
        self.bullet_capacity_text = self.gun_font.render(str(self.bullet_capacity), True, (255,255,255))
        self.reload_start_time = 0
        print(self.gun_idle, "FDSIKFJSDFOI")
        super().__init__(self.item_type, self.gun_type, [self.gun_idle, self.gun_firing, self.gun_reloading], self.gun_inventory)

    def display_gun(self, screen, bot_location):
        gun_idle_png = pygame.image.load(self.gun_idle)
        screen.blit(gun_idle_png, bot_location)


    def shoot(self, screen, mouse_position, bullet_sprite_group, obstacle_sprites, bot_location):
        if self.bullet_capacity > 0:
            self.bullet_capacity -= 1
            gun_firing_png = pygame.image.load(self.gun_firing)
            screen.blit(gun_firing_png, bot_location)
            print("hi")
            bullet = Bullet(mouse_position, gun_firing_png, obstacle_sprites, screen, None)
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
    def __init__(self, mouse_position, gun_image, obstacle_sprites, screen, custom_direction):
        super().__init__()
        self.screen = screen
        self.obstacle_sprites = obstacle_sprites
        self.image = pygame.Surface([12, 6])
        self.image.fill((255, 204, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (Bot.hitbox.x + gun_image.get_width(), Bot.hitbox.y)
        if custom_direction is None:
            direction = pygame.math.Vector2(mouse_position[0] - Bot.hitbox.x, mouse_position[1] - Bot.hitbox.y)
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
