import pygame

from entities.bar import Bar


class Score:
    def __init__(self, pos):
        self.txt = pygame.font.Font('assets/PirataOne-Regular.ttf', 32)
        self.pos = pos
        self.value = 1000
        self.barsize = (200, 30)
        self.bar = Bar(pos + (0, 100), self.barsize, 1000, self.value)

    # change la valeur d'une différence value_diff, attention mettre negatif pour enlever du score
    def change(self, value_diff):
        self.value += value_diff

    def draw(self, txt, pos, screen: pygame.Surface):
        txt_surf = self.txt.render(str(txt), True, (81, 44, 6) if pos[0] < 500 else (255, 255, 255))
        screen.blit(txt_surf, (pos[0], pos[1] + txt_surf.get_rect().height))
        self.bar.draw(self.pos, self.barsize, 1000, self.value, screen)
