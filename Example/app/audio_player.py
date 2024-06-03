import numpy as np
import sounddevice as sd

class AudioPlayer:

    def __init__(self):
        self.fs = 44100
        self.beep_duration = 10
        self.volume = 0.5
        self.frequency = 440
        self.stream = None
        self.is_playing = False

    def generate_tone(self):
        t = np.linspace(start=0, 
                        stop=self.beep_duration, 
                        num=int(self.fs * self.beep_duration), 
                        endpoint=False)
        tone = np.sin(2 * np.pi * self.frequency * t) * self.volume
        return tone

    def play_beep(self, frequency, volume, duration):
        self.frequency = frequency
        self.volume = volume
        self.beep_duration = duration
        sd.play(self.generate_tone(), self.fs)
