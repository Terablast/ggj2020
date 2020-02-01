import pygame as pg
import sys

from pygame.locals import *
import settings as st


class Game:
    def __init__(self):
        # Ecran
        pg.init()
        pg.display.set_caption('Platformer')
        self.DISPLAYSURF = pg.display.set_mode((st.WIDTH, st.HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.DISPLAYSURFcopy = self.DISPLAYSURF.copy()  # le self permet de créer un attribut de Game dans l'initialisation
        self.hero = Hero([30, 350], (30, 60), 'hero.png', st.HEROFOLDER)
        self.finalWidth, self.finalHeight = st.WIDTH, st.HEIGHT
        self.screenProgress = 0

    def run(self, level):

        self.loadLevel(level)
        running = True

        while running:
            level.printLevel(self.DISPLAYSURFcopy,
                             self.screenProgress)  # A optimiser pour pas faire la bouble a chaque fois, copie sur un frame
            self.printGrid(False)  # optionnel: True pour montrer la grille
            # print(self.screenProgress)
            self.events()
            self.hero.move()
            self.hero.contact(level.blockTab)
            self.screenProgress = self.hero.updateProgress(self.screenProgress)
            self.hero.printHero(self.DISPLAYSURFcopy)
            self.printFinalScreen()
            self.update()

    def printGrid(self, activate):
        if activate:
            for i in range(0, st.WIDTH, st.TILESIZE):
                pg.draw.line(self.DISPLAYSURFcopy, st.BLACK, (i, 0), (i, st.HEIGHT), 1)
            for j in range(0, st.WIDTH, st.TILESIZE):
                pg.draw.line(self.DISPLAYSURFcopy, st.BLACK, (0, j), (st.WIDTH, j), 1)
        else:
            pass

    def loadLevel(self, level):
        pass  # boucle pour la musique... autre chose? blocs dans la boucle

    def events(self):
        keyboardState = pg.key.get_pressed()
        if keyboardState[K_RIGHT]:
            self.hero.vx += 80
        elif keyboardState[K_LEFT]:
            self.hero.vx -= 80
        else:
            self.hero.vx = self.hero.vx / 2
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == VIDEORESIZE:
                screen = pg.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                self.finalWidth, self.finalHeight = screen.get_size()  # Variables globales :/
            if event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    self.hero.jump()

    def update(self):
        pg.display.update()
        pg.time.Clock().tick(st.FPS)

    def showStartScreen(self):
        print("Hey welcome")

    def showGoScreen(self):
        print("YOU LOSE!")
        pg.quit()
        sys.exit()

    def printFinalScreen(self):
        # On garde DISPLAYSURFcopy à la taille originale, resize sur DISPLAYSURF puis affiche
        self.DISPLAYSURF.blit(pg.transform.scale(self.DISPLAYSURFcopy, (self.finalWidth, self.finalHeight)),
                              (0, 0))  # ???


class Level:
    blockTab = []

    def __init__(self, backgroundImg, backgroundMusic, levelDesign, path):
        # Musique
        pg.mixer.music.load(path + backgroundMusic)
        pg.mixer.music.play(-1, 0.0)
        pg.mixer.music.set_volume(st.VOLUME)
        # image
        self.backgroundImage = pg.transform.scale(pg.image.load(path + backgroundImg), (st.WIDTH, st.HEIGHT))
        self.convertDesign(levelDesign, path)

    def convertDesign(self, levelDesign, path):
        # designFile=open(path+levelDesign,'r')
        X = 0
        Y = 0
        for line in open(path + levelDesign, 'r'):
            line = line.rstrip('\n')
            for symbol in line:
                # print(symbol)
                if symbol == "1":
                    pass
                elif symbol == "8":
                    self.blockTab.append(Stone((X, Y, st.TILESIZE, st.TILESIZE)))
                elif symbol == "4":
                    self.blockTab.append(Ladder((X, Y, st.TILESIZE, st.TILESIZE)))
                X += st.TILESIZE
            X = 0
            Y += st.TILESIZE

    def printLevel(self, surface, printBlock):
        surface.blit(self.backgroundImage, (0, 0))  # copie fond sur le provisoire
        for element in self.blockTab:
            element.printBlock(surface, printBlock)


class Hero:
    # wallJumpLeft=False #incorporer le wall jump avec compteur pour laisser du temps, et saut avec composante en x.
    # wallJumpRight=False
    forward = True  # true=forward false=backward
    vxMax = 500
    vyMax = 1000

    def jump(self):
        if not self.isJumping:
            self.isJumping = True
            self.vy -= 950

    def __init__(self, pos, size, imageName, path):  # Création personage
        self.picture = pg.transform.scale(pg.image.load(path + imageName), size)
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.vx = 0
        self.vy = 0
        self.isJumping = False
        # self.hitbox =[self.x,self.y,self.size[0],self.size[1]] pas update

    def printHero(self, surface):
        # pg.draw.rect(surface,st.RED,self.get_rect(),1)#dessine hitbox autour
        surface.blit(self.picture, (self.x, self.y))  # Attention position exacte vs coin haut gauche

    def move(self):
        self.vy += 140  # effet de la gravite

        if self.vx > self.vxMax:  # met une vitesse maximale dans les deux sens pour x et y
            self.vx = self.vxMax
        if self.vx < -self.vxMax:
            self.vx = -self.vxMax
        if self.vy > self.vyMax:
            self.vy = self.vyMax
        if self.vy < -self.vyMax:
            self.vy = -self.vyMax

        self.x += st.DT * self.vx
        self.y += st.DT * self.vy

    def updateProgress(self, screenProgress):
        if self.vx < 0:
            self.forward = False
        else:
            self.forward = True

        if (self.x > screenProgress + (st.WIDTH / 2)) and self.forward:
            return screenProgress + self.vx * st.DT

        if (self.x < screenProgress + (st.WIDTH / 3.5)) and (not self.forward):
            return screenProgress + (1.7 * self.vx)
        return screenProgress

    def contact(self, blockList):
        for block in blockList:
            if self.contactTete(block):
                self.vy = 0
                self.y = block.y + st.TILESIZE  # place en dessous du bloc et met vitesse  a zero
            # marche sur bloc
            if self.contactPieds(block):
                self.isJumping = False
                self.vy = 0
                self.y = block.y - self.size[1]
                self.canJump = True
            # appuie gauche
            if self.contactGauche(block):
                self.vx = 0
                self.x = block.x + st.TILESIZE

            # appuie droite
            if self.contactDroite(block):
                self.vx = 0
                self.x = block.x - self.size[0]

    def contactTete(self, block):
        # cogne tete si tete_y ds bloc                       et          coin haut gauche                        ou               haut droie est dedans
        return (block.y < self.get_top() < block.y + st.TILESIZE) and (
                    (block.x < self.get_left() < block.x + st.TILESIZE) or (
                        block.x < self.get_right() < block.x + st.TILESIZE))

    def contactPieds(self, block):
        return (block.y < self.get_bottom() < block.y + st.TILESIZE) and (
                    (block.x < self.get_left() < block.x + st.TILESIZE) or (
                        block.x < self.get_right() < block.x + st.TILESIZE))

    def contactGauche(self, block):
        return (block.x < self.get_left() < block.x + st.TILESIZE) and (
                    (block.y < self.get_top() < block.y + st.TILESIZE) or (
                        block.y < self.get_bottom() < block.y + st.TILESIZE) or (
                    (block.y < 0.5 * (self.get_bottom() + self.get_top()) < block.y + st.TILESIZE)))

    def contactDroite(self, block):
        return (block.x < self.get_right() < block.x + st.TILESIZE) and (
                    (block.y < self.get_top() < block.y + st.TILESIZE) or (
                        block.y < self.get_bottom() < block.y + st.TILESIZE) or (
                    (block.y < 0.5 * (self.get_bottom() + self.get_top()) < block.y + st.TILESIZE)))

    # Getters
    def get_top(self):
        return self.y

    def get_bottom(self):
        return self.y + self.size[1]

    def get_left(self):
        return self.x

    def get_right(self):
        return self.x + self.size[0]

    def get_rect(self):
        return (self.x, self.y, self.size[0], self.size[1])


class Block:
    x = 0
    y = 0

    def __init__(self, rect, texture):  # un rectangle pg.Rect
        self.x = rect[0]
        self.y = rect[1]
        # self.texture=texture
        self.blocSurface = pg.Surface((st.TILESIZE, st.TILESIZE))
        textureSized = pg.transform.scale(texture, (st.TILESIZE, st.TILESIZE))
        self.blocSurface.blit(textureSized, (0, 0))
        # self.blocSurface.convert_alpha(0.0)

    def printBlock(self, surface, screenProgress):
        surface.blit(self.blocSurface, (self.x - screenProgress, self.y))


class Stone(Block):
    textureStone = pg.image.load(st.IMAGEFOLDER + "stone.png")

    def __init__(self, rect):
        super().__init__(rect, self.textureStone)  # REVOIR APPEL CONSTRUCTEUR SUPERCLASSE!


class Ladder(Block):
    textureLadder = pg.image.load(st.IMAGEFOLDER + "ladder.png")

    # textureLadder.convert_alpha(0.0)
    def __init__(self, rect):
        super().__init__(rect, self.textureLadder)

    # Debut du jeu


g = Game()
g.showStartScreen()
lvl1 = Level('background1.png', 'background1.mp3', 'design.txt', st.LVL1FOLDER)  # 1er niveau
print("RUN")
g.run(lvl1)
g.showGoScreen()
