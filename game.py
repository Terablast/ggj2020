import datetime
import sys

from entities.boats import Boats
from entities.incident import *
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
    INCIDENT_CHANCE = 0.4
    INCIDENT_DELAY = 1

    def __init__(
            self,
            game_options: GameOptions
    ) -> None:
        if game_options is not None:
            self.options = game_options
        else:
            self.options = GameOptions()
        self.c = pygame.time.Clock()

    def start(self):
        pygame.init()

        # Set up the drawing window
        # pygame.display.set_mode(
        #   [self.options.width, self.options.height],
        #    flags=pygame.FULLSCREEN if self.options.fullscreen else 0
        # )
        screen_resized = pygame.display.set_mode((self.options.width, self.options.height),
                                                 pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
                                                 | pygame.FULLSCREEN if self.options.fullscreen else 0)
        screen = pygame.Surface((1920, 1080), )

        wanna_play = True
        while wanna_play:
            start_menu = True
            img_background = pygame.image.load('assets/menu.jpg').convert()
            screen.blit(img_background, (0, 0))
            self.draw_resized_screen(screen, screen_resized)

            while start_menu:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (
                            event.type == pygame.KEYDOWN and
                            event.key == pygame.K_F4 and
                            event.mod & pygame.KMOD_ALT != 0):
                        running = False
                        sys.exit()

                    if event.type == pygame.VIDEORESIZE:
                        screen_resized = pygame.display.set_mode(event.dict['size'],
                                                                 pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
                                                                 | pygame.FULLSCREEN if self.options.fullscreen else 0)
                        self.options.width, self.options.height = screen_resized.get_size()
                        self.draw_resized_screen(screen, screen_resized)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        start_menu = False
                pygame.display.flip()

            img_background = pygame.image.load('assets/background.jpg').convert()
            img_rain = pygame.image.load('assets/rain.png').convert_alpha()

            boats = Boats(screen, (0, 0))
            ladders = Ladders(screen, (0, 0))

            pirate_left = Pirate(
                screen,
                (200, -200),
                True,  # joueur gauche
                {
                    'up': pygame.K_w,
                    'right': pygame.K_d,
                    'down': pygame.K_s,
                    'left': pygame.K_a,
                    'action': pygame.K_SPACE
                }
            )

            pirate_right = Pirate(
                screen,
                (1700, -200),
                False,  # joueur droite
                {
                    'up': pygame.K_UP,
                    'right': pygame.K_RIGHT,
                    'down': pygame.K_DOWN,
                    'left': pygame.K_LEFT,
                    'action': pygame.K_l,
                }
            )

            last_incident = datetime.datetime.now()
            last_incident_type = None

            running = True
            while running:
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (
                            event.type == pygame.KEYDOWN and
                            event.key == pygame.K_F4 and
                            event.mod & pygame.KMOD_ALT != 0):
                        running = False

                    if event.type == pygame.VIDEORESIZE:
                        screen_resized = pygame.display.set_mode(event.dict['size'],
                                                                 pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
                                                                 | pygame.FULLSCREEN if self.options.fullscreen else 0)
                        self.options.width, self.options.height = screen_resized.get_size()

                boats.update()

                since_last_incident = datetime.datetime.now() - last_incident

                if since_last_incident.seconds >= Game.INCIDENT_DELAY:
                    last_incident = datetime.datetime.now()

                    if random.random() <= Game.INCIDENT_CHANCE:
                        potential_incident_types = [
                            Fire.__name__,
                            Flood.__name__
                        ]

                        if last_incident_type is not None:
                            potential_incident_types.remove(last_incident_type)

                        incident_type = random.choice(potential_incident_types)

                        if Fire.__name__ == incident_type:
                            last_incident_type = Fire.__name__

                            other_fires_left = [x for x in pirate_left.incidents if type(x) is Fire]
                            if len(other_fires_left) < len(Fire.POSITIONS_LEFT):
                                pirate_left.incidents.append(Fire(pirate_left, screen))

                            other_fires_right = [x for x in pirate_right.incidents if type(x) is Fire]
                            if len(other_fires_right) < len(Fire.POSITIONS_RIGHT):
                                pirate_right.incidents.append(Fire(pirate_right, screen))

                        elif Flood.__name__ == incident_type:
                            last_incident_type = Flood.__name__

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

                # screen.blit(img_rain, (0, -1080 + (
                #   pygame.time.get_ticks() % 1080
                # )))

                self.draw_resized_screen(screen, screen_resized)
                # Flip the display
                pygame.display.flip()

                self.c.tick(60)
                # print(self.c.get_fps())

                if pirate_left.score.value <= 0.0:
                    running = False
                    right_win_go_screen = True

                    img_background = pygame.image.load('assets/player_right_win.jpg').convert()
                    screen.blit(img_background, (0, 0))
                    self.draw_resized_screen(screen, screen_resized)
                    while right_win_go_screen:

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (
                                    event.type == pygame.KEYDOWN and
                                    event.key == pygame.K_F4 and
                                    event.mod & pygame.KMOD_ALT != 0):
                                running = False

                            if event.type == pygame.VIDEORESIZE:
                                screen_resized = pygame.display.set_mode(event.dict['size'],
                                                                         pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
                                                                         | pygame.FULLSCREEN if self.options.fullscreen else 0)
                                self.options.width, self.options.height = screen_resized.get_size()
                                self.draw_resized_screen(screen, screen_resized)
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                wanna_play = True
                                right_win_go_screen = False
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                wanna_play = False
                                right_win_go_screen = False

                        pygame.display.flip()
                if pirate_right.score.value <= 0.0:
                    running = False
                    left_win_go_screen = True

                    img_background = pygame.image.load('assets/player_left_win.jpg').convert()
                    screen.blit(img_background, (0, 0))
                    self.draw_resized_screen(screen, screen_resized)
                    while left_win_go_screen:

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (
                                    event.type == pygame.KEYDOWN and
                                    event.key == pygame.K_F4 and
                                    event.mod & pygame.KMOD_ALT != 0):
                                running = False

                            if event.type == pygame.VIDEORESIZE:
                                screen_resized = pygame.display.set_mode(event.dict['size'],
                                                                         pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
                                                                         | pygame.FULLSCREEN if self.options.fullscreen else 0)
                                self.options.width, self.options.height = screen_resized.get_size()
                                self.draw_resized_screen(screen, screen_resized)
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                wanna_play = True
                                left_win_go_screen = False
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                wanna_play = False
                                left_win_go_screen = False

                        pygame.display.flip()
        # Done! Time to quit.
        pygame.quit()

    def draw_resized_screen(self, screen, screen_resized):
        if self.options.width == 1920 and self.options.height == 1080:
            screen_resized.blit(screen, (0, 0))
        else:
            screen_resized.blit(pygame.transform.scale(screen, (self.options.width, self.options.height)), (0, 0))
