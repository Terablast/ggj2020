import pygame

MAX_SPEED = 7

class Pirate(pygame.sprite.Sprite):
    def __init__(
            self,
            screen,
            pos,
            controls,
            *groups
    ):
        super().__init__(*groups)

        self.screen = screen
        self.img = pygame.image.load('./assets/pirate.png').convert_alpha()
        self.mask = pygame.mask.from_surface(pygame.image.load('./assets/pirate.png').convert_alpha())
        self.rect: pygame.Rect = self.img.get_rect()

        self.controls = controls

        self.rect.left = pos[0]
        self.rect.top = pos[1]

        self.vx = 0
        self.vy = 0

    def update(
            self,
            keys
    ):
        if keys[self.controls['up']]:
            self.vy -= 5

        if keys[self.controls['right']]:
            self.vx = min(self.vx + 1, MAX_SPEED)

        if keys[self.controls['down']]:
            pass

        if keys[self.controls['left']]:
            self.vx = max(self.vx - 1, -MAX_SPEED)

        if not keys[self.controls['left']] and not keys[self.controls['right']]:
            # Lorsqu'on ne tient pas gauche ni droite, on perds notre momentum horizontal
            if self.vx > 0:
                self.vx = max(self.vx - 1, 0)
            elif self.vx < 0:
                self.vx = min(self.vx + 1, 0)

        self.vy = max(self.vy - 0.1, 0)

        self.rect.left += self.vx
        self.rect.top += self.vy

    def draw(self):
        self.screen.blit(self.img, self.rect)
