import pygame
import map
import random
import sprites

class Bot(pygame.sprite.Sprite):
    # we put this here so the inventory doesn't need to call superclass init method, therefore the parameters for init
    # arent messed up

    def __init__(self, position, sprite_group, obstacle_sprites, screen):
        super().__init__(sprite_group)
        self.engage_sounds = [pygame.mixer.Sound("audio\\Enemy_Contact.mp3"),
                              pygame.mixer.Sound("audio\\Enemy_Contact_2.mp3")]
        self.already_said_enemy_contact = False
        self.return_fire = False
        self.return_fire_counter = 0
        self.position = position
        self.screen = screen
        self.mouse_clicked = False
        self.clock = pygame.time.Clock()
        self.player_hitpoints = 100
        self.armor_value = 0
        self.inventory = Inventory(self.player_hitpoints, self.armor_value)
        self.sprite_right = pygame.image.load("sprites\\player\\right\\right_0.png")
        self.hit_marker_sound = pygame.mixer.Sound("audio\\hit_marker.mp3")
        self.image = self.sprite_right
        self.rect = self.image.get_rect(topleft=(position[0]-514,position[1]+138))
        self.x_direction = 0
        self.y_direction = 0
        self.obstacle_sprites = obstacle_sprites
        self.death_sounds = [pygame.mixer.Sound("audio\\death_sound.wav"),
                             pygame.mixer.Sound("audio\\death_sound_2.wav"),
                             pygame.mixer.Sound("audio\\death_sound_3.wav")]
        self.gun_reloading_sound = pygame.mixer.Sound("audio\\gun_reload.mp3")

        # new method i found online to change the hitbox so that its smaller
        self.hitbox = self.rect.inflate(-5, -5)

        self.reloading_sound_played = None
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

    def collisions(self, direction, bullet_sprites, player_position):
        for sprite in bullet_sprites:
            if sprite.rect.colliderect(self.hitbox):
                # return fire by the AI
                self.return_fire = True
                if self.already_said_enemy_contact is False:
                    channel6 = pygame.mixer.Channel(5)
                    channel6.play(self.engage_sounds[random.randint(0,1)])
                    self.already_said_enemy_contact = True
                channel4 = pygame.mixer.Channel(3)
                channel4.play(self.hit_marker_sound)
                if self.inventory.armor_value == 0:
                    self.inventory.player_hitpoints -= sprite.bullet_damage
                else:
                    self.inventory.armor_value -= sprite.bullet_damage
                    if self.inventory.armor_value < 0:
                        self.inventory.player_hitpoints += sprite.bullet_damage
                        self.inventory.armor_value = 0
                sprite.kill()
                print("WOW IT HAPPENED")
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

    def update(self, bullet_sprites, player_position, bot_group):
        if self.return_fire:
            for bot in bot_group:

                if bot.hitbox.colliderect(pygame.Rect(player_position[0] - 500, player_position[1] - 500, 1000, 1000)):
                    bot.return_fire = True
                    bot.already_said_enemy_contact = True

            self.return_fire_counter += 1
            if self.return_fire_counter % 45 == 0:
                self.inventory.weapon.shoot(self.screen, player_position, bullet_sprites, self.obstacle_sprites, self.hitbox)
        if self.inventory.player_hitpoints <= 0:
            channel7 = pygame.mixer.Channel(6)
            channel7.play(self.death_sounds[random.randint(0, 2)])
            self.kill()
        self.walking_direction_timer += 1
        if self.walking_direction_timer % 350 == 0:
            self.walking_direction += 1
        if self.walking_direction > 4:
            self.walking_direction = 0
        self.move_ai()
        if self.inventory.weapon:
            if self.inventory.weapon.bullet_capacity <= 0:
                if not self.reloading_sound_played:
                    channel = pygame.mixer.Channel(6)
                    channel.play(self.gun_reloading_sound)
                    self.reloading_sound_played = True
                self.inventory.weapon.reload()
        if self.return_fire == False:
            self.hitbox.x += self.x_direction
            self.hitbox.y += self.y_direction
        self.collisions("horizontal", bullet_sprites, player_position)
        self.collisions("vertical", bullet_sprites, player_position)
        self.rect.topleft = self.hitbox.topleft  # Update rect position to match hitbox
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
        self.gun_firing_sound = pygame.mixer.Sound("audio\\gun_firing.mp3")
        # if gun_bullets is not None: self.bullet_capacity = gun_bullets
        self.max_bullet_capacity = self.bullet_capacity = gun_types.get(self.gun_type, {}).get("bullet_capacity")
        self.bullet_damage = gun_types.get(self.gun_type, {}).get("bullet_damage")
        self.reload_time = gun_types.get(self.gun_type, {}).get("reload_time")
        self.gun_font = pygame.font.SysFont("arial", 35)
        self.bullet_capacity_text = self.gun_font.render(str(self.bullet_capacity), True, (255,255,255))
        self.reload_start_time = 0
        super().__init__(self.item_type, self.gun_type, [self.gun_idle, self.gun_firing, self.gun_reloading], self.gun_inventory)

    def display_gun(self, screen, bot_location):
        gun_idle_png = pygame.image.load(self.gun_idle)
        screen.blit(gun_idle_png, bot_location)


    def shoot(self, screen, player_position, bullet_sprite_group, obstacle_sprites, bot_location):
        if self.bullet_capacity > 0:
            channel = pygame.mixer.Channel(7)
            channel.set_volume(0.5)
            channel.play(self.gun_firing_sound)
            self.bullet_capacity -= 1
            gun_firing_png = pygame.image.load(self.gun_firing)
            screen.blit(gun_firing_png, bot_location)
            print("hi")
            # mouse position replaced with player position
            bullet = Bullet(player_position, gun_firing_png, obstacle_sprites, screen, None, bot_location, self.bullet_damage)
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
    def __init__(self, mouse_position, gun_image, obstacle_sprites, screen, custom_direction, hitbox, damage):
        super().__init__()
        self.bullet_damage = damage
        self.screen = screen
        self.obstacle_sprites = obstacle_sprites
        self.image = pygame.Surface([12, 6])
        self.image.fill((255, 204, 0))
        self.rect = self.image.get_rect()
        self.hitbox = hitbox
        self.rect.center = (self.hitbox.x + gun_image.get_width(), self.hitbox.y)
        if custom_direction is None:
            # calculate custom direction:
            # RANDOM CALCULATION WITH DEVIATION SIMILAR TO SHOTGUN
            original_direction = pygame.math.Vector2(mouse_position[0] - self.hitbox.x, mouse_position[1] - self.hitbox.y)
            deviation_x = random.uniform(-30, 30)
            deviation_y = random.uniform(0, 30)
            direction = original_direction + pygame.math.Vector2(deviation_x,deviation_y)
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