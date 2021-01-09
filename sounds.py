from pygame import mixer


class Sounds:
    def __init__(self):
        self.volume = 100
        shotgun_shot_sound_file = "data/sounds/shot.wav"
        self.shotgun_shot_sound = mixer.Sound(shotgun_shot_sound_file)
        self.shotgun_shot_sound.set_volume(self.volume)

    def shotgun_shot(self):
        shotgun_shot_sound_file = "data/sounds/shot.wav"
        self.shotgun_shot_sound = mixer.Sound(shotgun_shot_sound_file)
        self.shotgun_shot_sound.set_volume(self.volume)
        return self.shotgun_shot_sound.play()

    # def hit(self):
    #     hit_sound_file = "data/sounds/hit.wav"
    #     hit_sound = mixer.Sound(hit_sound_file)
    #     return hit_sound.play()
    def set_volume(self, value):
        self.volume = value
        self.shotgun_shot_sound.set_volume(value / 100)

    def get_volume(self):
        return self.volume
