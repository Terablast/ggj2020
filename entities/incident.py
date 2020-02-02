import random

import pygame


class Incident(pygame.sprite.Sprite):
    def __init__(
            self,
            img,
            pirate,
            screen,
            *groups
    ):
        super().__init__(*groups)

        if self.pos is None:
            self.pos = (0, 0)

        self.screen = screen
        self.img = img

        self.pirate = pirate

        self.rect: pygame.Rect = self.img.get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]

    def draw(self):
        self.screen.blit(self.img, self.rect)


class Fire(Incident):
    FRAMES = []
    POSITIONS_LEFT = [
        (194, 487),
        (650, 487),
        (193, 623),
        (693, 623),
    ]

    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        if len(Fire.FRAMES) == 0:
            for i in range(1, 11):
                Fire.FRAMES.append(
                    pygame.image.load('assets/fire/frame (' + str(i) + ').png').convert_alpha()
                )

        img = Fire.FRAMES[0]

        other_fires = [x for x in pirate.incidents if type(x) is Fire]

        potential_positions = [x for x in Fire.POSITIONS_LEFT]

        for of in other_fires:
            potential_positions.remove(of.pos)

        self.pos = random.choice(potential_positions)

        super().__init__(
            img,
            pirate,
            screen,
            *groups
        )

    def draw(self):
        self.img = Fire.FRAMES[(pygame.time.get_ticks() // 50) % 10]
        super().draw()


class Flood(Incident):
    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        img = pygame.image.load('assets/flood.jpg').convert_alpha()

        super().__init__(
            img,
            pirate,
            screen,
            *groups
        )


class Tear(Incident):
    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        img = pygame.image.load('assets/tear.png').convert()
        super().__init__(
            self,
            img,
            pirate,
            screen,
            groups
        )
