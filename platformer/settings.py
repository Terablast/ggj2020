import os  # folder managment

# Game options & settings
VOLUME = 0.0

# Dimesions de départ
WIDTH = 1024  # 32*32
HEIGHT = 576  # 32*18
FPS = 60
DT = 1 / FPS
TILESIZE = 32
# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TRANSPARENT = (255, 255, 255, 0.8)

# Assets folders
GAMEFOLDER = os.path.dirname(__file__)
LEVELFOLDER = os.path.join(GAMEFOLDER, "level/")
LVL1FOLDER = os.path.join(LEVELFOLDER, "level1/")  # level1
EFFECTFOLDER = os.path.join(GAMEFOLDER, "effect/")
IMAGEFOLDER = os.path.join(GAMEFOLDER, "image/")
FONTFOLDER = os.path.join(GAMEFOLDER, "font/")
HEROFOLDER = os.path.join(GAMEFOLDER, "hero/")
