"""
date: may 21st, 2023
name: william
description: this program creates a game where a user-controlled pacman can eat cherries displayed on the screen
"""

import pygame, myPacmanSprites

pygame.init()
screen = pygame.display.set_mode((640, 480))


def main():
    # create display name
    pygame.display.set_caption("Pacman game")
    # initialize entities
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    # create 10 cherries by appending through a list 10 times, and one movable pacman
    cherries = []
    for i in range(10):
        cherries.append(myPacmanSprites.Cherry(screen))
    CherrySprites = pygame.sprite.Group(cherries)
    pacman = myPacmanSprites.Pacman(screen)
    PacmanSprite = pygame.sprite.Group(pacman)
    # create clock
    keepGoing = True
    clock = pygame.time.Clock()
    # main game loop
    while keepGoing:
        # set fps
        clock.tick(30)
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            # if any of the arrow keys are pressed, it will move the pacman in the corresponding direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.go_up()
                elif event.key == pygame.K_DOWN:
                    pacman.go_down()
                elif event.key == pygame.K_LEFT:
                    pacman.go_left()
                elif event.key == pygame.K_RIGHT:
                    pacman.go_right()
            # using a bit of my own research, this part of the code detects when cherries in the cherry group are
            # colliding with each other, and generates a new set of 10 cherries if this is the case
            for cherry in CherrySprites:
                collision = pygame.sprite.spritecollide(cherry, CherrySprites, False)
                if len(collision) > 1:
                    cherries = []
                    for i in range(10):
                        cherries.append(myPacmanSprites.Cherry(screen))
                    CherrySprites = pygame.sprite.Group(cherries)
                # if the pacman collides with a cherry, it is removed from the screen
                if cherry.rect.colliderect(pacman.rect):
                    CherrySprites.remove(cherry)
        # refresh screen
        CherrySprites.clear(screen, background)
        PacmanSprite.clear(screen, background)
        CherrySprites.draw(screen)
        PacmanSprite.draw(screen)
        PacmanSprite.update(screen)
        pygame.display.flip()
    # close the game window
    pygame.quit()


# call the main function
main()
