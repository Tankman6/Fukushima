import player
import pygame
import sprites
import menu

main_menu = True


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Fukushima 2044")
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        self.main_menu = True

        self.sprites = sprites.Sprites(self.screen)
        self.inventory = player.Inventory(self.screen)

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


game_loop = Game()
game_loop.start()
