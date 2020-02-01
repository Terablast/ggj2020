import pygame
import math
import random
from entities.incident import Tear
from entities.incident import Fire
from entities.incident import Flood

#from ... import GameOptions HELP PLS



MAX_SPEED = 4
JUMP_VELOCITY = -8
GRAVITY = 0.25


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
            'normal': pygame.image.load('./assets/pirate.png').convert_alpha(),
            'crouch': pygame.image.load('./assets/pirate_crouch.png').convert_alpha()
        }

        self.img = self.sprites['normal']
        self.mask = pygame.mask.from_surface(pygame.image.load('./assets/pirate_mask.png').convert_alpha())
        self.rect: pygame.Rect = self.img.get_rect()

        self.controls = controls

        self.rect.left = pos[0]
        self.rect.top = pos[1]

        self.vx = 0
        self.vy = 0

        self.jumping = False

        self.initial_pos = pos
        self.respawn_timer = -1

        self.imminent = True #True si un incident peut arriver (active la generation aleatoire d'un incident)
        self.is_player_left=is_player_left
        self.event_list=[]

    def update(
            self,
            keys,
            ladders
    ):
        on_ladder = pygame.sprite.collide_mask(self, ladders) is not None

        if keys[self.controls['up']] and (
                not self.jumping
                or on_ladder
        ):
            self.vy += JUMP_VELOCITY

        if keys[self.controls['right']]:
            self.vx = min(self.vx + 1, MAX_SPEED)

        if keys[self.controls['down']]:
            self.img = self.sprites['crouch']
        else:
            self.img = self.sprites['normal']

        if keys[self.controls['left']]:
            self.vx = max(self.vx - 1, -MAX_SPEED)

        if not keys[self.controls['left']] and not keys[self.controls['right']]:
            # Lorsqu'on ne tient pas gauche ni droite, on perds notre momentum horizontal
            if self.vx > 0:
                self.vx = max(self.vx - 1, 0)
            elif self.vx < 0:
                self.vx = min(self.vx + 1, 0)

        self.vy += GRAVITY

        if self.vy < -10: self.vy = -10
        if self.vy > 10: self.vy = 10

        self.rect.left += self.vx
        self.rect.top += self.vy


        if self.rect.top > 3000 and self.respawn_timer < 0:
            print('drowned!')
            self.respawn_timer = 250

        if self.respawn_timer > 0:
            print('respawning!', self.respawn_timer)
            self.respawn_timer -= 1

        if self.respawn_timer == 0:
            self.rect.left = self.initial_pos[0]
            self.rect.top = self.initial_pos[1]
            self.respawn_timer = -1

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
            self.vy = 0
            self.jumping = True

    def draw(self):
        self.screen.blit(self.img, self.rect)

    def clamp(n, smallest, largest):
        return max(smallest, min(n, largest))


    def new_event_check(self): #retourne true si un evenement arrive
        if self.imminent:
            if random.random()<60*0.05: #???? GameOptions.c.get_fps()
                self.imminent=False
                return True
            else:
                return False

        else:
            return False

    def add_event(self):
        N=math.ceil(random.random()*8)
        for i in self.event_list:
            if abs(i.label_number-N)<0.01: #si meme numero: si on essaie de creer un event qui exite deja. dif pour eviter comparaison entre 1.0 et 1 etc...
                N+=1

        if N==1 or N==2:
            self.event_list.append(Tear(self.is_player_left,N))
        if N == 3 or N == 4 or N==5 or N==6:
            self.event_list.append(Fire(self.is_player_left, N))
        if N==7 or N==8:
            self.event_list.append(Flood(self.is_player_left,N))