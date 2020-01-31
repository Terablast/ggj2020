import contextlib
import random
import pymunk

with contextlib.redirect_stdout(None):
    import pygame


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

        space = pymunk.Space()
        space.gravity = 0, 10

        ball = pymunk.Body(1, 1666)
        ball.position = 50, 100

        ball_poly = pymunk.Poly.create_box(ball, radius=50)
        space.add(ball, ball_poly)

        # Run until the user asks to quit
        running = True
        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                        event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT != 0):
                    running = False

            space.step(0.02)

            # Fill the background with white
            screen.fill((255, 255, 255))

            # Draw a solid blue circle in the center
            pygame.draw.circle(screen, (0, 0, 255), (int(ball.position.x), int(ball.position.y)), 50)

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()
