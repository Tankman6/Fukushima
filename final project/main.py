import pygame, sprites, map, player, items


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Fukushima 2044")
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        self.sprites = sprites.Sprites(self.screen)
        self.cursor_image = pygame.image.load("sprites\\Crosshairs_Red.png")
        self.background_audio = pygame.mixer.music.load("audio\\background-ambience.mp3")
        pygame.mixer.music.play(loops=-1)

    def start(self):
        while self.keepGoing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.keepGoing = False

            self.screen.fill((0, 0, 0))
            self.sprites.update()
            # MOVE THIS CODE TO THE PLAYER UPDATE FUNCTION PROBABLY
            self.screen.blit(self.cursor_image, player.Player.print_crosshair(self))
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)


game_loop = Game()
game_loop.start()
