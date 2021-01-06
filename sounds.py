from pygame import mixer


class Sounds:
    def shotgun_shot(self):
        shotgun_shot_sound_file = "data/sounds/shot.wav"
        shotgun_shot_sound = mixer.Sound(shotgun_shot_sound_file)
        return shotgun_shot_sound.play()

    def hit(self):
        hit_sound = mixer.Sound("data/sounds/shot.wav")
        return hit_sound.play()
