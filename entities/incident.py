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
    def __init__(
            self,
            pirate,
            screen,
            *groups
    ):
        img = pygame.image.load('assets/fire.png').convert_alpha()

        super().__init__(
            self,
            img,
            pirate,
            screen,
            *groups
        )


class Flood(Incident):
    def __init__(
            self,
            pirate,
            pos,
            screen,
            *groups
    ):
        img = pygame.image.load('assets/flood.jpg').convert_alpha()

        super().__init__(
            self,
            img,
            pirate,
            screen,
            *groups
        )


'''
class Tear(Incident):
    def __init__(self,
                 is_player_left,
                 label_number):
        img = pygame.image.load('assets/flood.jpg').convert()
        super().__init__(
            self,
            img,
            is_player_left,
            label_number
        )
'''
