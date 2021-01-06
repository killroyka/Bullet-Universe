from pygame import mixer


class Sounds:
    def shotgun_shot(self):
        return mixer.Sound("data/sounds/shot.wav")

    def hit(self):
        return mixer.Sound("data/sounds/hit.wav")
