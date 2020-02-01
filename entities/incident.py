import pygame
import random


class Incident:
    def __init__(self,
                 img,
                is_player_left, #pour calculer avec le no de l'incident ou se passe l'incident
                label_number # nombre de 1 a 8 indiquant le type d'incident
                ):

        self.pos=[0,0] # a refaire
        self.img=img
        self.label_number=label_number

        self.rect: pygame.Rect = self.img.get_rect()
        self.rect.left = self.pos[0]
        self.rect.top = self.pos[1]


    def draw(self):
        self.screen.blit(self.img, self.rect)


class Fire(Incident):
    def __init__(self,
                 is_player_left,
                 label_number):
        img = pygame.image.load('assets/fire.png').convert()
        super().__init__(self,
                         img,
                         is_player_left,
                         label_number
                         )


class Flood(Incident):
        def __init__(self,
                     is_player_left,
                     label_number):
            img = pygame.image.load('assets/flood.jpg').convert()
            super().__init__(self,
                         img,
                         is_player_left,
                         label_number
                         )


class Tear(Incident):
    def __init__(self,
                 is_player_left,
                 label_number):
        img = pygame.image.load('assets/flood.jpg').convert()
        super().__init__(self,
                         img,
                         is_player_left,
                         label_number
                         )

