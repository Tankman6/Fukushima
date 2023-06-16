"""
Author: Christine Wei
Date: June 5, 2023
Description: Menu
"""

# this will be menu
# include settings, help and start
# maybe make a save feature

# IMPORTS
import pygame
import os
pygame.init()

os.chdir(os.getcwd())

# Entities
WIDTH = 1080
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
timer = pygame.time.Clock()

main_menu = False
font = pygame.font.Font('graphics/Retro Gaming.ttf', 24)


class Button:
    def __init__(self, screen, txt, pos):
        self.text = txt
        self.pos = pos
        self.screen = screen

        self.button = pygame.image.load("graphics/UI/button1.png")
        self.button_rect = self.button.get_rect()
        self.button_rect.centerx = self.pos[0]
        self.button_rect.centery = self.pos[1]

        self.big_button = pygame.transform.scale(self.button, (self.button.get_width()*1.1, self.button.get_height()*1.1))
        self.big_button_rect = self.big_button.get_rect()
        self.big_button_rect.centerx = self.pos[0]
        self.big_button_rect.centery = self.pos[1]

    def draw(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.big_button, self.big_button_rect)
        else:
            screen.blit(self.button, self.button_rect)

        text = font.render(self.text, True, 'black')
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

    def press(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False


def draw_game():
    menu_btn = Button(screen, "Menu", [900, 600])
    menu_btn.draw()
    if menu_btn.press():
        menu = True
    else:
        menu = False

    return menu


def draw_menu():
    # Draw Manu Background
    menu_bg = pygame.Surface((880, 520))
    menu_bg.set_alpha(50)
    menu_bg.fill((255, 255, 255))
    screen.blit(menu_bg, (100, 100))

    # Resume game / exit menu Button
    resume_btn = Button(screen, "RESUME", [screen.get_width()/2, screen.get_height()/2 - 50])
    resume_btn.draw()
    if resume_btn.press():
        menu = False
    else:
        menu = True

        # Return to main menu button
        main_btn = Button(screen, "MAIN MENU", [screen.get_width() / 2, screen.get_height() / 2 + 50])
        main_btn.draw()

    # Quit Menu Button
    quit_btn = Button(screen, "QUIT", [screen.get_width() / 2, screen.get_height() / 2 + 150])
    quit_btn.draw()
    if quit_btn.press():
        quit_game = True
    else:
        quit_game = False

    return [menu, quit_game]


run = True
while run:
    screen.fill((114, 117, 27))
    background = pygame.image.load('fuki4.png')
    # screen.blit(background, (0, -1600))

    timer.tick(fps)
    if main_menu:
        main_menu = draw_menu()[0]
        if draw_menu()[1]:
            run = False
    else:
        main_menu = draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()