import vlc

PATH_TO_POUET = "/home/crysteo/content/sounds/faster.wav"

player = vlc.MediaPlayer(PATH_TO_POUET)

class pouet_sound:
    def __init__(self,fifo_callback):
        self.callback = fifo_callback

    def execute(self,data):
        if not player.is_playing():
            vlc.MediaPlayer(PATH_TO_POUET).play()
