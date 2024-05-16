import numpy as np
import sounddevice as sd

class AudioPlayer:
    """
    Play a simple beep sound using the sounddevice library (from ChatGPT)
    """

    def __init__(self):
        self.fs = 44100
        self.beep_duration = 1
        self.pause_duration = 1
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
        silence = np.zeros(int(self.fs * self.pause_duration))
        return np.concatenate((tone, silence))

    def start_beep(self):
        if not self.is_playing:
            self.is_playing = True
            tone = self.generate_tone()

            def callback(outdata, frames, time, status):
                nonlocal tone
                outdata[:] = tone[:frames].reshape(-1, 1)
                tone = np.roll(tone, -frames)

            self.stream = sd.OutputStream(channels=1, callback=callback, samplerate=self.fs, blocksize=len(tone))
            self.stream.start()

    def stop_beep(self):
        if self.stream and self.is_playing:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            self.is_playing = False
