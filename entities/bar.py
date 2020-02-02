import pygame

class Bar:
    def __init__(self,pos,size,value_max,current_value):
        Bar.pos=pos
        self.x=pos[0]
        self.y=pos[1]
        self.Lx=size[0]
        self.Ly=size[1]
        self.size=size #(Lx,Ly)
        self.value_max=value_max
        self.current_value=current_value

    def draw(self,pos,size,value_max,current_value,display_surf):
        pygame.draw.rect(display_surf,(0,0,0),(self.x,self.y,self.Lx,self.Ly),0)
        pygame.draw.rect(display_surf, (255, 0, 0), (self.x+0.05*self.Lx, self.y+0.05*self.Ly, self.Lx*0.9, self.Ly*0.9), 0)
        pygame.draw.rect(display_surf, (0, 255, 0), (self.x+0.05*self.Lx, self.y+0.05*self.Ly, self.Lx*0.9*(current_value/value_max), self.Ly*0.9), 0)
