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

        self.bar_size = (self.rect.width, 10)

        self.bar = Bar(
            (self.rect.bottomleft),
            self.bar_size,
            self.life_points_max,
            self.life_points
        )

    def draw(self):
        self.screen.blit(self.img, self.rect)
        self.bar.draw(self.rect.bottomleft, (self.rect.width, self.rect.height), self.life_points_max, self.life_points, self.screen)


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

        #effet sonore:
        self.sound_effect_thunder = pygame.mixer.Sound('assets/music/thunder.wav')
        self.sound_effect_thunder.set_volume(0.10)
        self.sound_effect_thunder.play()
        self.sound_effect = pygame.mixer.Sound('assets/music/fire.wav')
        self.sound_effect.set_volume(0.02)
        self.sound_effect.play(-1)

        self.life_points = 100
        self.life_points_max = 100
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
    FRAMES = []

    POSITIONS_LEFT = [
        (284, 910),
        (600, 910),
    ]

    POSITIONS_RIGHT = [
        (1272, 910),
        (1590, 910),
    ]

    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        if len(Flood.FRAMES) == 0:
            for i in range(1, 11):
                Flood.FRAMES.append(
                    pygame.image.load('./assets/flood/frame (' + str(i) + ').png').convert_alpha()
                )

        img = Flood.FRAMES[0]

        other_floods = [x for x in pirate.incidents if type(x) is Flood]
        potential_positions = [x for x in (Flood.POSITIONS_LEFT if pirate.is_player_left else Flood.POSITIONS_RIGHT)]
        for of in other_floods:
            potential_positions.remove(of.pos)
        self.mask = pygame.mask.from_surface(
            pygame.image.load('./assets/flood/mask.png').convert_alpha())
        self.pos = random.choice(potential_positions)

        #effet sonore:
        self.sound_effect = pygame.mixer.Sound('assets/music/water.wav')
        self.sound_effect.set_volume(0.02)
        self.sound_effect.play(-1)

        self.life_points = 100
        self.life_points_max = 100
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
            self.pirate.touch_flood = self
            if self.pirate.rect.x > self.rect.x + self.rect.width / 2:
                self.pirate.touch_flood_right = True
            else:
                self.pirate.touch_flood_right = False

    def draw(self):
        self.img = Flood.FRAMES[(pygame.time.get_ticks() // 50) % 10]
        super().draw()


class Scurvy(Incident):
    FRAMES = []

    POSITIONS_LEFT = [
        (280, 849),
        (653, 788),
    ]

    POSITIONS_RIGHT = [
        (1220, 788),
        (1577, 855),
    ]

    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        if len(Scurvy.FRAMES) == 0:
            for i in range(1, 11):
                Scurvy.FRAMES.append(
                    pygame.image.load('./assets/scurvy/frame (' + str(i) + ').png').convert_alpha()
                )

        img = Scurvy.FRAMES[0]

        other_oranges = [x for x in pirate.incidents if type(x) is Scurvy]
        potential_positions = [x for x in (Scurvy.POSITIONS_LEFT if pirate.is_player_left else Scurvy.POSITIONS_RIGHT)]
        for of in other_oranges:
            potential_positions.remove(of.pos)
        self.mask = pygame.mask.from_surface(
            pygame.image.load('./assets/scurvy/mask.png').convert_alpha())
        self.pos = random.choice(potential_positions)
        self.life_points = 50
        self.life_points_max = 50

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
            self.pirate.touch_flood = self
            if self.pirate.rect.x > self.rect.x + self.rect.width / 2:
                self.pirate.touch_flood_right = True
            else:
                self.pirate.touch_flood_right = False

    def draw(self):
        self.img = Scurvy.FRAMES[(pygame.time.get_ticks() // 50) % 10]
        super().draw()


class Tear(Incident):
    FRAMES_LEFT = []
    FRAMES_RIGHT = []

    POSITIONS_LEFT = [
        (75, 84),
        (514, 90),
        (222, 355),
        (620, 366),
    ]

    POSITIONS_RIGHT = [
        (1049, 85),
        (1483, 88),
        (1569, 372),
        (1200, 350),
    ]

    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        if len(Tear.FRAMES_LEFT) == 0:
            for i in range(1, 11):
                Tear.FRAMES_LEFT.append(
                    pygame.image.load('./assets/tear/frameright (' + str(i) + ').png').convert_alpha()
                )
                Tear.FRAMES_RIGHT.append(
                    pygame.image.load('./assets/tear/frameleft (' + str(i) + ').png').convert_alpha()
                )

        img = Tear.FRAMES_LEFT[0] if pirate.is_player_left else Tear.FRAMES_RIGHT[0]

        other_floods = [x for x in pirate.incidents if type(x) is Tear]
        potential_positions = [x for x in (Tear.POSITIONS_LEFT if pirate.is_player_left else Tear.POSITIONS_RIGHT)]
        for of in other_floods:
            potential_positions.remove(of.pos)
        self.mask = pygame.mask.from_surface(
            pygame.image.load('./assets/tear/mask.png').convert_alpha())
        self.pos = random.choice(potential_positions)

        self.life_points = 100
        self.life_points_max = 100
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
            self.pirate.touch_flood = self
            if self.pirate.rect.x > self.rect.x + self.rect.width / 2:
                self.pirate.touch_flood_right = True
            else:
                self.pirate.touch_flood_right = False

    def draw(self):
        self.img = Tear.FRAMES_LEFT[(pygame.time.get_ticks() // 50) % 10] if self.pirate.is_player_left else Tear.FRAMES_RIGHT[(pygame.time.get_ticks() // 50) % 10]
        super().draw()
