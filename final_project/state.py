import pygame
import os
import player
import sprites

pygame.init()
os.chdir(os.getcwd())

# ENTITIES
font = pygame.font.Font('graphics/Retro Gaming.ttf', 24)


class Button:
    def __init__(self, screen, txt, pos):
        self.text = txt
        self.pos = pos
        self.screen = screen

        self.button = pygame.image.load("graphics/UI/button1.png").convert_alpha()
        self.button_rect = self.button.get_rect()
        self.button_rect.centerx = self.pos[0]
        self.button_rect.centery = self.pos[1]

        self.big_button = pygame.transform.scale(self.button,
                                                 (self.button.get_width() * 1.1, self.button.get_height() * 1.1))
        self.big_button_rect = self.big_button.get_rect()
        self.big_button_rect.centerx = self.pos[0]
        self.big_button_rect.centery = self.pos[1]

    def draw(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            # self.screen.blit(self.big_button, self.big_button_rect)
            self.screen.blit(self.button, self.button_rect)
        else:
            self.screen.blit(self.button, self.button_rect)

        text = font.render(self.text, True, 'black')
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

    def press(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False


class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Fukushima 2044")
        self.clock = pygame.time.Clock()
        self.keepGoing, self.playing = True, True
        self.actions = {"left": False, "right": False, "up": False, "down": False, "action1": False, "start": False}
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.inventory = player.Inventory(self.screen)

    def update(self, delta_time, actions):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()


class Title(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)

    def update(self, delta_time, actions):
        if actions["Level1"]:
            new_state = Level1(self.game)
            new_state.enter_state()
        self.game.reset_keys()

    def render(self, screen):
        # Draw manu
        screen.fill((114, 117, 27))
        background = pygame.image.load('graphics/fuki4.png')
        screen.blit(background, (0, 0))
        no_menu = None
        button = None

        # Level 1
        level1_btn = Button(screen, "LEVEL 1", [screen.get_width() / 2, screen.get_height() / 2 + 50])
        level1_btn.draw()

        # Level 2
        level2_btn = Button(screen, "LEVEL 2", [screen.get_width() / 2, screen.get_height() / 2 + 150])
        level2_btn.draw()

        # Events
        if level1_btn.press():
            self.game.actions["Level1"] = True
        if level2_btn.press():
            self.game.actions["Level2"] = True


class PauseMenu(State):
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        State.__init__(self, game)

        # Resume game / exit menu Button
        self.resume_btn = Button(self.screen, "RESUME", [self.screen.get_width()/2, self.screen.get_height()/2-50])

        # Return to main menu button
        self.title_btn = Button(self.screen, "MAIN MENU", [self.screen.get_width()/2, self.screen.get_height()/2+50])

        # Quit Menu Button
        self.quit_btn = Button(self.screen, "QUIT", [self.screen.get_width()/2, self.screen.get_height()/2+150])

    def update(self, delta_time, actions):
        if actions["Title"]:
            new_state = Title(self.game)
            new_state.enter_state()
        if actions["return"]:
            self.exit_state()

        self.game.reset_keys()

    def render(self, screen):
        # Render game screen
        self.prev_state.render(screen)

        # Render the menu
        self.resume_btn.draw()
        self.title_btn.draw()
        self.quit_btn.draw()

    def transition_state(self):
        # Events (Check button presses)
        if self.resume_btn.press():
            self.game.actions["return"] = True
        if self.title_btn.press():
            self.game.actions["Title"] = True
            new_state = Title(self.game)
            new_state.enter_state()
        if self.quit_btn.press():
            self.game.keepGoing = False


class Level1(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        pygame.mixer.init()
        self.screen = game.screen
        # self.clock = pygame.time.Clock()
        self.sprites = sprites.Sprites(self.screen)
        self.inventory = player.Inventory(screen=self.screen)

    def update(self, delta_time, actions):
        if actions["Pause"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.sprites.update()

        dt = self.clock.tick() / 1000
        self.sprites.run(dt)
        self.game.reset_keys()

    def render(self, screen):
        menu_btn = Button(screen, "Menu", [950, 100])
        menu_btn.button = pygame.transform.scale(menu_btn.button, (menu_btn.button.get_width()*0.7, menu_btn.button.get_height()*0.7))
        menu_btn.draw()

        # Events (Check button presses)
        if menu_btn.press():
            self.game.actions["Pause"] = True


class Level2(State):
    def __init__(self, game):
        self.game = game
        State.__init__(self, game)
        pygame.mixer.init()
        self.game = game
        self.screen = game.screen
        # self.clock = pygame.time.Clock()
        self.sprites = sprites.Sprites(self.screen)
        self.inventory = player.Inventory(screen=self.screen)

    def update(self, delta_time, actions):
        if actions["Pause"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.sprites.update()

        dt = self.clock.tick() / 1000
        self.sprites.run(dt)
        self.game.reset_keys()

    def render(self, screen):
        menu_btn = Button(screen, "Menu", [900, 600])
        menu_btn.draw()

        # Events (Check button presses)
        if menu_btn.press():
            self.game.actions["Pause"] = True
