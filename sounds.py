from main import *

from pygame import mixer


class Sounds:
    def shotgun_shot(self):
        return mixer.Sound("shot.wav")

    def hit(self):
        return mixer.Sound("hit.wav")
