import math

import pygame

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

        self.sprites = {
            'punch_right': pygame.image.load('./assets/pirate/punch_right.png').convert_alpha(),
            'punch_left': pygame.image.load('./assets/pirate/punch_left.png').convert_alpha(),
            'normal': pygame.image.load('./assets/pirate/pirate.png').convert_alpha(),
            'crouch': pygame.image.load('./assets/pirate/pirate_crouch.png').convert_alpha(),
            'climb1': pygame.image.load('./assets/pirate/pirate_grimpe1.png').convert_alpha(),
            'climb2': pygame.image.load('./assets/pirate/pirate_grimpe2.png').convert_alpha(),
            'water_right': pygame.image.load('./assets/pirate/water_right.png').convert_alpha(),
            'water_left': pygame.image.load('./assets/pirate/water_left.png').convert_alpha()
        }

        self.img = self.sprites['normal']
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

        self.is_player_left = is_player_left

        self.touch_fire = None
        self.touch_fire_right = True

        self.is_looking_right = True
        # initialise le score:
        if is_player_left:
            scorex = 50
        else:
            scorex = 1650
        self.score = Score((scorex, 50))
        self.incidents = []

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
            self.img = self.sprites['crouch']
        elif on_ladder and keys[self.controls['up']]:
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                self.img = self.sprites['climb1']
            else:
                self.img = self.sprites['climb2']
        else:
            self.img = self.sprites['normal']

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
                self.img = self.sprites['water_left'] if self.touch_fire_right else self.sprites['water_right']
                self.touch_fire.life_points -= 1  # trouver quel feu a eteindre et enlever 1 life_point
                if self.touch_fire.life_points <= 0.0:
                    self.incidents.remove(self.touch_fire)
                    self.touch_fire = None

            elif not self.touch_fire:
                self.img = self.sprites['punch_right'] if self.is_looking_right else self.sprites['punch_left']

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
