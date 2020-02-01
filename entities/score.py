import pygame


class Score:
    def __init__(self, pos):
        self.txt = pygame.font.Font('assets/PirataOne-Regular.ttf', 32)
        self.pos = pos
        self.value = 100

    def change(self,
               value_diff):  # change la valeur d'une différence value_diff, attention mettre negatif pour enlever du score
        self.value += value_diff

    def draw(self, txt, pos, screen):
        txt_surf = self.txt.render(str(txt), True, (81, 44, 6))
        txt_rect = txt_surf.get_rect()
        screen.blit(txt_surf, txt_rect)
