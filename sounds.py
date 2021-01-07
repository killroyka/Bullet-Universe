from pygame import mixer


class Sounds:
    def shotgun_shot(self):
        shotgun_shot_sound_file = "data/sounds/shot.wav"
        shotgun_shot_sound = mixer.Sound(shotgun_shot_sound_file)
        shotgun_shot_sound.set_volume(0.2)
        return shotgun_shot_sound.play()

    # def hit(self):
    #     hit_sound_file = "data/sounds/hit.wav"
    #     hit_sound = mixer.Sound(hit_sound_file)
    #     return hit_sound.play()
