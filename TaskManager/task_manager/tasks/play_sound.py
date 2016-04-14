import vlc

PATH_TO_SOUNDS = "/home/crysteo/content/sounds/"

player = vlc.MediaPlayer()

class sound_buffer:
    def __init__(self,sound_list):
        self.bufsize = len(sound_list)
        self.sounds = sound_list
        self.counter = -1

    def get_next_sound(self):
        self.counter += 1
        if self.counter == self.bufsize:
            self.counter = 0
        return self.sounds[self.counter]

bonjour_sounds_buffer = sound_buffer([ 'bonjour.wav', 'ipluggi.wav', 'irobot.wav' ])
danger_sounds_buffer = sound_buffer(['DANGEEER.wav'])
laugh_sounds_buffer = sound_buffer(['lol.wav'])
ok_sounds_buffer = sound_buffer([ 'ok.wav', 'ok2.wav', 'ok3.wav', 'ok4.wav' ])

sounds = { '0' : bonjour_sounds_buffer,
          '1' : danger_sounds_buffer,
          '2' : laugh_sounds_buffer,
          '3' : ok_sounds_buffer
         }

class play_sound:
    def __init__(self,fifo_callback):
        self.player = vlc.MediaPlayer()
        self.callback = fifo_callback

    def execute(self,data):
        if data[1] in sounds and not self.player.is_playing():
            self.player = vlc.MediaPlayer(PATH_TO_SOUNDS + sounds[data[1]].get_next_sound())
            self.player.play()
        randomdata = [ '1','2','3','4' ]
        self.callback(42,randomdata)

