import pygame


class Boats(pygame.sprite.Sprite):
    def __init__(self, screen, pos, *groups):
        super().__init__(*groups)

        self.screen = screen
        self.img = pygame.image.load('./assets/boat_mask.png').convert_alpha()
        self.mask = pygame.mask.from_surface(pygame.image.load('./assets/boat_mask.png').convert_alpha())
        self.rect: pygame.Rect = self.img.get_rect()

        self.rect.left = pos[0]
        self.rect.top = pos[1]

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.img, self.rect)



