"""
Author: Christine Wei
Date: June 5, 2023
Description: Menu
"""

# IMPORTS
import pygame
import os
pygame.init()

os.chdir(os.getcwd())

font = pygame.font.Font('graphics/Retro Gaming.ttf', 24)


class Button(pygame.sprite.Sprite):
    def __init__(self, groups, screen, txt, pos):
        self.screen = screen

        self.pos = pos
        self.text = txt
        self.screen = screen

        self.button = pygame.image.load("graphics/UI/button1.png")
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
            self.screen.blit(self.big_button, self.big_button_rect)
        else:
            self.screen.blit(self.button, self.button_rect)

        text = font.render(self.text, True, 'black')
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

    def press(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.screen.blit(self.button, self.button_rect)
            return True
        else:
            return False


class Buttons(pygame.sprite.Group):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.button = pygame.image.load("graphics/sprites/UI/button1.png")
        self.button_rect = self.button.get_rect()

        self.big_button = pygame.transform.scale(self.button,
                                                 (self.button.get_width() * 1.1, self.button.get_height() * 1.1))
        self.big_button_rect = self.big_button.get_rect()


class Menu:
    def __init__(self, screen):
        # Draw Manu Background
        self.menu_bg = pygame.Surface((880, 520))
        self.menu_bg.set_alpha(50)
        self.menu_bg.fill((255, 255, 255))

        self.screen = screen

        self.screen.blit(self.menu_bg, (100, 100))
        self.buttons = Buttons(self.screen)

    def draw(self):
        self.buttons.draw(0, 0)


class MainMenu(Menu):
    pass


class GameMenu(Menu):
    pass


class Level1:
    def __init__(self):
        super.__init__()

    def start(self):
        while self.keepGoing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.keepGoing = False

            self.screen.fill((0, 0, 0))
            self.sprites.update()

            dt = self.clock.tick() / 1000
            self.sprites.run(dt)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)


class Level2:
    def __init__(self):
        super.__init__()

    def start(self):
        while self.keepGoing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.keepGoing = False

            self.screen.fill((0, 0, 0))
            self.sprites.update()

            dt = self.clock.tick() / 1000
            self.sprites.run(dt)

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)