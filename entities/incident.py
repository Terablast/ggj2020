import random

import pygame

from entities.bar import Bar


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

        self.bar_size=(100, 10)
        self.life_points = 100
        #self.rect.bottomleft
        self.bar = Bar((self.rect.bottomleft[0]+70,self.rect.bottomleft[1]+5), self.bar_size, 1000, self.life_points)

    def draw(self):
        self.screen.blit(self.img, self.rect)
        self.bar.draw(self.rect.bottomleft, (self.rect.width, self.rect.height), 100, self.life_points, self.screen)


class Fire(Incident):
    FRAMES = []

    POSITIONS_LEFT = [
        (144, 487),
        (550, 487),
        (593, 623),
        (93, 623),
    ]

    POSITIONS_RIGHT = [
        (1110, 487),
        (1530, 487),
        (1050, 623),
        (1600, 623),
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
                    pygame.image.load('./assets/fire/frame (' + str(i) + ').png').convert_alpha()
                )

        img = Fire.FRAMES[0]

        other_fires = [x for x in pirate.incidents if type(x) is Fire]

        potential_positions = [x for x in (Fire.POSITIONS_LEFT if pirate.is_player_left else Fire.POSITIONS_RIGHT)]

        for of in other_fires:
            potential_positions.remove(of.pos)
        self.mask = pygame.mask.from_surface(pygame.image.load('./assets/fire/mask.png').convert_alpha())
        self.pos = random.choice(potential_positions)

        super().__init__(
            img,
            pirate,
            screen,
            *groups
        )

    def update(self):
        collision_point = self.mask.overlap(
            self.pirate.mask,
            ((self.pirate.rect.x - self.rect.x), (self.pirate.rect.y - self.rect.y))
        )

        if collision_point is not None:
            self.pirate.touch_fire = self
            if self.pirate.rect.x > self.rect.x + self.rect.width / 2:
                self.pirate.touch_fire_right = True
            else:
                self.pirate.touch_fire_right = False


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
