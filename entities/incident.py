import pygame

class Incident:
    def __init__(self,
                pos, #position: coordonnees pour afficher l'incident
                img
                ):

        self.pos=pos
        self.img=img
        self.rect: pygame.Rect = self.img.get_rect()

        self.rect.left = pos[0]
        self.rect.top = pos[1]


    def draw(self):
        self.screen.blit(self.img, self.rect)

class Fire(Incident):
    def __init__(self,
                 pos):
        img = pygame.image.load('assets/fire.png').convert()
        super().__init__(self,
                         pos,
                         img)


class Flood(Incident):
        def __init__(self,
                     pos):
            img = pygame.image.load('assets/flood.jpg').convert()
            super().__init__(self,
                             pos,
                             img)

