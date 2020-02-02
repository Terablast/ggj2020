import math

import pygame

from entities.incident import Scurvy
from entities.score import Score

MAX_X_SPEED = 7
MAX_Y_SPEED = 10
JUMP_VELOCITY = -8
GRAVITY = 0.50


class Pirate(pygame.sprite.Sprite):
    def __init__(
            self,
            screen,
            pos,
            is_player_left,  # true si joueur gauche, aide a localiser les evenements sur le bon bateau
            controls,
            *groups

    ):
        super().__init__(*groups)

        self.screen = screen

        self.is_player_left = is_player_left
        if self.is_player_left:
            self.sprites = {
                'punch_right': pygame.image.load('./assets/pirate/red/punch_right.png').convert_alpha(),
                'punch_left': pygame.image.load('./assets/pirate/red/punch_left.png').convert_alpha(),
                'normal': pygame.image.load('./assets/pirate/red/pirate.png').convert_alpha(),
                'crouch': pygame.image.load('./assets/pirate/red/pirate_crouch.png').convert_alpha(),
                'climb1': pygame.image.load('./assets/pirate/red/pirate_climb1.png').convert_alpha(),
                'climb2': pygame.image.load('./assets/pirate/red/pirate_climb2.png').convert_alpha(),
                'water_right': pygame.image.load('./assets/pirate/red/water_right.png').convert_alpha(),
                'water_left': pygame.image.load('./assets/pirate/red/water_left.png').convert_alpha(),
                'bucket_right': pygame.image.load('./assets/pirate/red/ecope_right.png').convert_alpha(),
                'bucket_left': pygame.image.load('./assets/pirate/red/ecope_left.png').convert_alpha(),
                'punch_right_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/punch_right_scorbut.png').convert_alpha(),
                'punch_left_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/punch_left_scorbut.png').convert_alpha(),
                'normal_scorbut': pygame.image.load('./assets/pirate/red/scorbut/pirate_scorbut.png').convert_alpha(),
                'crouch_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/pirate_crouch_scorbut.png').convert_alpha(),
                'climb1_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/pirate_climb1_scorbut.png').convert_alpha(),
                'climb2_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/pirate_climb2_scorbut.png').convert_alpha(),
                'water_right_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/water_right_scorbut.png').convert_alpha(),
                'water_left_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/water_left_scorbut.png').convert_alpha(),
                'bucket_right_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/ecope_right_scorbut.png').convert_alpha(),
                'bucket_left_scorbut': pygame.image.load(
                    './assets/pirate/red/scorbut/ecope_left_scorbut.png').convert_alpha()
            }
        else:
            self.sprites = {
                'punch_right': pygame.image.load('./assets/pirate/blue/punch_right_blue.png').convert_alpha(),
                'punch_left': pygame.image.load('./assets/pirate/blue/punch_left_blue.png').convert_alpha(),
                'normal': pygame.image.load('./assets/pirate/blue/pirate_blue.png').convert_alpha(),
                'crouch': pygame.image.load('./assets/pirate/blue/pirate_crouch_blue.png').convert_alpha(),
                'climb1': pygame.image.load('./assets/pirate/blue/pirate_climb1_blue.png').convert_alpha(),
                'climb2': pygame.image.load('./assets/pirate/blue/pirate_climb2_blue.png').convert_alpha(),
                'water_right': pygame.image.load('./assets/pirate/blue/water_right_blue.png').convert_alpha(),
                'water_left': pygame.image.load('./assets/pirate/blue/water_left_blue.png').convert_alpha(),
                'bucket_right': pygame.image.load('./assets/pirate/blue/water_right_blue.png').convert_alpha(),
                'bucket_left': pygame.image.load('./assets/pirate/blue/water_left_blue.png').convert_alpha(),
                'punch_right_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/punch_right_blue_scorbut.png').convert_alpha(),
                'punch_left_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/punch_left_blue_scorbut.png').convert_alpha(),
                'normal_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/pirate_blue_scorbut.png').convert_alpha(),
                'crouch_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/pirate_crouch_blue_scorbut.png').convert_alpha(),
                'climb1_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/pirate_climb1_blue_scorbut.png').convert_alpha(),
                'climb2_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/pirate_climb2_blue_scorbut.png').convert_alpha(),
                'water_right_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/water_right_blue_scorbut.png').convert_alpha(),
                'water_left_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/water_left_blue_scorbut.png').convert_alpha(),
                'bucket_right_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/water_right_blue_scorbut.png').convert_alpha(),
                'bucket_left_scorbut': pygame.image.load(
                    './assets/pirate/blue/scorbut/water_left_blue_scorbut.png').convert_alpha()
            }

        self.incidents = []

        self.img = self.sprites['normal' + ('_scorbut' if self.has_scurvy() else '')]
        self.mask = pygame.mask.from_surface(pygame.image.load('./assets/pirate/pirate_mask.png').convert_alpha())
        self.rect: pygame.Rect = self.img.get_rect()

        self.controls = controls

        self.rect.left = pos[0]
        self.rect.top = pos[1]

        self.vx = 0
        self.vy = 0

        self.jumping = False

        self.initial_pos = pos
        self.respawn_timer = -1

        self.touch_fire = None
        self.touch_fire_right = True
        self.touch_flood = None
        self.touch_flood_right = True

        self.is_looking_right = True
        # initialise le score:
        if is_player_left:
            scorex = 50
        else:
            scorex = 1660
        self.score = Score((scorex, 50))

    def update(
            self,
            keys,
            ladders
    ):
        on_ladder = pygame.sprite.collide_mask(self, ladders) is not None

        if keys[self.controls['up']]:
            if on_ladder:
                self.vy = JUMP_VELOCITY / 3
            elif not self.jumping:
                self.vy += JUMP_VELOCITY

        if keys[self.controls['right']]:
            self.vx = min(self.vx + 1, MAX_X_SPEED)
            self.is_looking_right = True

        if keys[self.controls['down']]:
            self.img = self.sprites['crouch' + ('_scorbut' if self.has_scurvy() else '')]
        elif on_ladder and keys[self.controls['up']]:
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                self.img = self.sprites['climb1' + ('_scorbut' if self.has_scurvy() else '')]
            else:
                self.img = self.sprites['climb2' + ('_scorbut' if self.has_scurvy() else '')]
        else:
            self.img = self.sprites['normal' + ('_scorbut' if self.has_scurvy() else '')]

        if keys[self.controls['left']]:
            self.vx = max(self.vx - 1, -MAX_X_SPEED)
            self.is_looking_right = False

        if not keys[self.controls['left']] and not keys[self.controls['right']]:
            # Lorsqu'on ne tient pas gauche ni droite, on perds notre momentum horizontal
            if self.vx > 0:
                self.vx = max(self.vx - 0.5, 0)
            elif self.vx < 0:
                self.vx = min(self.vx + 0.5, 0)

        if keys[self.controls['action']]:
            if self.touch_fire is not None:
                self.img = self.sprites[
                    'water_left' + ('_scorbut' if self.has_scurvy() else '')] if self.touch_fire_right else self.sprites[
                    'water_right' + ('_scorbut' if self.has_scurvy() else '')]
                self.touch_fire.life_points -= 1  # trouver quel feu a eteindre et enlever 1 life_point
                if self.touch_fire.life_points <= 0.0:
                    self.touch_fire.sound_effect.stop()
                    self.incidents.remove(self.touch_fire)
                    self.touch_fire = None
            elif self.touch_flood is not None:
                self.img = self.sprites[
                    'bucket_left' + ('_scorbut' if self.has_scurvy() else '')] if self.touch_flood_right else \
                self.sprites['bucket_right' + ('_scorbut' if self.has_scurvy() else '')]
                self.touch_flood.life_points -= 1  # trouver quel inondation a ecoper et enlever 1 life_point
                if self.touch_flood.life_points <= 0.0:
                    self.incidents.remove(self.touch_flood)
                    try:
                        self.touch_flood.sound_effect.stop()
                    except AttributeError:
                        pass
                    self.touch_flood = None

            else:  # elif not self.touch_fire:
                self.img = self.sprites[
                    'punch_right' + ('_scorbut' if self.has_scurvy() else '')] if self.is_looking_right else self.sprites[
                    'punch_left' + ('_scorbut' if self.has_scurvy() else '')]

        self.vy += GRAVITY

        if self.vy < -MAX_Y_SPEED: self.vy = -MAX_Y_SPEED
        if self.vy > MAX_Y_SPEED: self.vy = MAX_Y_SPEED

        self.rect.left += self.vx
        self.rect.top += self.vy

        if self.rect.top > 3000 and self.respawn_timer < 0:
            self.respawn_timer = 250

        if self.respawn_timer > 0:
            self.respawn_timer -= 1

        if self.respawn_timer == 0:
            self.rect.left = self.initial_pos[0]
            self.rect.top = self.initial_pos[1]
            self.respawn_timer = -1

        self.score.value = max(0, self.score.value - 0.01 - (len(self.incidents) * 0.1))

        self.touch_fire = None
        self.touch_flood = None

        for incident in self.incidents:
            incident.update()

    def collide(self, mask):
        dx = mask.overlap_area(self.mask, (self.rect.x + 1, self.rect.y)) \
             - mask.overlap_area(self.mask, (self.rect.x - 1, self.rect.y))
        dy = mask.overlap_area(self.mask, (self.rect.x, self.rect.y + 1)) \
             - mask.overlap_area(self.mask, (self.rect.x, self.rect.y - 1))

        if dx == 0 and dy == 0:
            # Si on touche à rien, on est dans l'air:
            self.jumping = True
            return

        if dx > 0:
            self.vx = 0
            self.rect.left -= 1

        if dx < 0:
            self.vx = 0
            self.rect.left += 1

        if dy > 0:
            self.rect.top -= 1
            self.vy = 0
            self.jumping = False

        if dy < 0:
            self.rect.top += 1
            self.vy = 1
            self.jumping = True

    def draw(self):
        for incident in self.incidents:
            incident.draw()

        self.score.draw(math.floor(self.score.value), self.score.pos, self.screen)
        self.screen.blit(self.img, self.rect)

    def has_scurvy(self):
        return Scurvy in [type(x) for x in self.incidents]
