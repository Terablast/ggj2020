import contextlib
import random
import pygame

from entities.boats import Boats
from entities.pirate import Pirate


class GameOptions:
    def __init__(
            self,
            verbose=False,
            fullscreen=False,
            width=600,
            height=800
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

        boat = Boats(screen, (0, 0))
        pirate = Pirate(screen, (1000, 800), {
            'up': pygame.K_UP,
            'right': pygame.K_RIGHT,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
        })

        c = pygame.time.Clock()

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

            boat.update()
            pirate.update(
                pygame.key.get_pressed()
            )

            print (pygame.sprite.collide_mask(pirate, boat))

            if pygame.sprite.collide_mask(pirate, boat) is not None:
                screen.blit(img_background, (5, 0))
            else:
                screen.blit(img_background, (0, 0))

            boat.draw()
            pirate.draw()

            # Flip the display
            pygame.display.flip()

            c.tick()
            #print(c.get_fps())

        # Done! Time to quit.
        pygame.quit()
