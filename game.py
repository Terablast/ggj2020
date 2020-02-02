import datetime

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
        start_menu=True
        img_background = pygame.image.load('assets/menu.jpg').convert()
        screen.blit(img_background, (0, 0))
        pygame.display.flip()
        while start_menu:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    start_menu=False

        img_background = pygame.image.load('assets/background.jpg').convert()

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
                        event.mod & pygame.KMOD_ALT != 0
                ):
                    running = False

            boats.update()

            since_last_incident = datetime.datetime.now() - last_incident

            if since_last_incident.seconds >= Game.INCIDENT_DELAY:
                last_incident = datetime.datetime.now()

                if random.random() <= Game.INCIDENT_CHANCE:
                    # IT'S HAPPENING

                    potential_incident_types = [
                        Fire.__name__,
                        Flood.__name__
                    ]

                    if last_incident_type is not None:
                        potential_incident_types.remove(last_incident_type)

                    incident_type = random.choice(potential_incident_types)

                    if Fire.__name__ == incident_type:
                        print('FIRE')
                        last_incident_type = Fire.__name__

                        other_fires_left = [x for x in pirate_left.incidents if type(x) is Fire]

                        if len(other_fires_left) < len(Fire.POSITIONS_LEFT):
                            pirate_left.incidents.append(Fire(pirate_left, screen))

                        # pirate_right.incidents.append(Fire(pirate_right, screen))

                        pass  # Lightning has struck: FIRE!
                    elif Flood.__name__ == incident_type:
                        print('FLOOD')
                        last_incident_type = Flood.__name__
                        pass  # The hull broke: FLOOD!
                else:
                    print('the calm before the storm')

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
