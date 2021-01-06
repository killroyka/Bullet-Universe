from main import *

from pygame import mixer


class Sounds:
    def shotgun_shot(self):
        return mixer.Sound("shot.wav")