import sounddevice as sd
import numpy as np

fs = 44100  
duration = 2 
frequency = 440.0 
volume = 0.01  

t = np.linspace(0, duration, int(fs * duration), endpoint=False)
waveform = volume * np.sin(2 * np.pi * frequency * t)

def test_device(device_id):
    try:
        sd.default.device = device_id
        device_info = sd.query_devices(device_id)
        output_channels = device_info['max_output_channels']
        print(f"Teste Gerät {device_id}: {device_info['name']} mit {output_channels} Ausgabekanälen")
        
        # Abspielen des Sounds
        sd.play(waveform, samplerate=fs)
        sd.wait()
        print(f"Ton erfolgreich auf Gerät {device_id} abgespielt: {device_info['name']}\n\n")
    except Exception as e:
        print(f"Fehler beim Testen des Geräts {device_id}: {e}\n\n")

# Durchlaufen und Testen aller Geräte
for device_id in range(len(sd.query_devices())):
    test_device(device_id)