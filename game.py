import contextlib
import random
import pygame

from entities.boats import Boats
from entities.ladders import Ladders
from entities.pirate import Pirate


class GameOptions:
    def __init__(
            self,
            verbose=False,
            fullscreen=False,
            width=600,
            height=800,
    ) -> None:
        super().__init__()
        self.verbose = verbose
        self.fullscreen = fullscreen
        self.width = width if width is not None else 800
        self.height = height if height is not None else 600


class Game:
    def __init__(
            self,
            game_options: GameOptions
    ) -> None:
        if game_options is not None:
            self.options = game_options
        else:
            self.options = GameOptions()
        self.c = pygame.time.Clock()

    def print_verbose(self, msg):
        if self.options.verbose:
            print(msg)

    def start(self):
        self.print_verbose('Verbosity is on!')

        pygame.init()

        # Set up the drawing window
        screen = pygame.display.set_mode(
            [self.options.width, self.options.height],
            flags=pygame.FULLSCREEN if self.options.fullscreen else 0
        )

        img_background = pygame.image.load('assets/background.jpg').convert()

        boats = Boats(screen, (0, 0))
        ladders = Ladders(screen, (0, 0))


        pirate_left = Pirate(screen,
                             (200, -200),
                             True, #joueur gauche
                             {
                            'up': pygame.K_w,
                            'right': pygame.K_d,
                            'down': pygame.K_s,
                            'left': pygame.K_a,
                            })

        pirate_right = Pirate(screen,
                              (1700, -200),
                              False, #joueur droite
                               {
                                'up': pygame.K_UP,
                                'right': pygame.K_RIGHT,
                                'down': pygame.K_DOWN,
                                'left': pygame.K_LEFT,
                              })



        # Run until the user asks to quit
        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and
                        event.key == pygame.K_F4 and
                        event.mod & pygame.KMOD_ALT != 0
                ):
                    running = False

            boats.update()

            pirate_left.update(
                pygame.key.get_pressed(),
                ladders
            )
            pirate_right.update(
                pygame.key.get_pressed(),
                ladders
            )

            pirate_left.collide(boats.mask)
            pirate_right.collide(boats.mask)

            screen.blit(img_background, (0, 0))

            boats.draw()
            pirate_left.draw()
            pirate_right.draw()

            # Flip the display
            pygame.display.flip()

            self.c.tick(120)
            # print(self.c.get_fps())

        # Done! Time to quit.
        pygame.quit()
