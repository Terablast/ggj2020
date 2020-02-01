import pygame


class Boat(pygame.sprite.Sprite):
    def __init__(self, screen, pos, *groups):
        super().__init__(*groups)

        self.screen = screen
        self.img = pygame.image.load('./assets/boat_mask.png')
        self.mask = pygame.mask.from_surface(pygame.image.load('./assets/boat_mask.png'))
        self.rect: pygame.Rect = self.img.get_rect()

        self.rect.left = pos[0]
        self.rect.top = pos[1]

    def update(self):
        self.rect.left += 2

    def draw(self):
        self.screen.blit(self.img, self.rect)



