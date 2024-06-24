from .audio_player import AudioPlayer

from pynput import keyboard
import time
import random
import tempfile as tfile
import csv


class Procedure():

    def __init__(self, startlevel, signal_length):
        """The parent class for the familiarization, the main procedure and the short version

        Args:
            startlevel (float): starting level of procedure in dBHL
            signal_length (float): length of played signals in seconds
        """
        self.ap = AudioPlayer()
        self.startlevel = startlevel
        self.level = startlevel
        self.signal_length = signal_length
        self.frequency = 1000
        self.zero_dbhl = 0.00002 # zero_dbhl in absolute numbers. Needs to be calibrated!
        self.tone_heard = False
        self.freq_bands = ['125', '250', '500', '1000', '2000', '4000', '8000']


    def dbhl_to_volume(self, dbhl):
        """calculate dBHL into absolute numbers

        Args:
            dbhl (float): value in dBHL

        Returns:
            float: value in absolute numbers
        """
        return self.zero_dbhl * 10 ** (dbhl / 10)
    

    def key_press(self, key):
        if key == keyboard.Key.space:
            self.tone_heard = True
            print("Tone heard!")
        
        


    def play_tone(self):
        """set tone_heard to False, play beep, then wait max 4s for keypress.
        If key is pressed, set tone_heard to True.
        Then wait for around about 2s (randomized).
        """
        self.tone_heard = False
        print("playing tone..")
        self.ap.play_beep(self.frequency, self.dbhl_to_volume(self.level), self.signal_length, 'l')
        listener = keyboard.Listener(on_press=self.key_press, on_release=None)
        listener.start()
        current_wait_time = 0
        max_wait_time = 4000 # in ms 
        step_size = 50 # in ms
        while current_wait_time < max_wait_time and self.tone_heard == False: # wait for keypress
            time.sleep(step_size / 1000)
            current_wait_time += step_size
        listener.stop()
        print("listener stopped.")
        self.ap.stop()
        if self.tone_heard == False:
            print("Tone not heard :(")
        sleep_time = abs(random.gauss(2, 1.2)) # non negative random number
        time.sleep(sleep_time) # wait before next tone is played. #TODO test times

    
    def create_temp_csv(self):
        """creates a temporary CSV file with the relevant frequency bands as a header
        and NaN in the second line as starting value for each band.

        Returns:
            str: name of temporary file
        """
        with tfile.NamedTemporaryFile(mode='w+', delete=False, newline='', suffix='.csv') as temp_file:
            # Define the CSV writer
            csv_writer = csv.writer(temp_file)

            # Write header
            csv_writer.writerow(self.freq_bands)

            # Write value NaN for each frequency in second row
            csv_writer.writerow(['NaN' for i in range(len(self.freq_bands))])

            return temp_file.name
        
        
    def add_to_temp_csv(self, value, frequency, temp_filename):
        """add a value in for a specific frequency to the temporary csv file

        Args:
            value (str): level in dBHL at specific frequency
            frequency (str): frequency where value should be added
            temp_filename (str): name of temporary csv file
        """
        with open(temp_filename, mode='r', newline='') as temp_file:
            dict_reader = csv.DictReader(temp_file)
            freq_dict = next(dict_reader)
            freq_dict[frequency] = value
            print(freq_dict)

        with open(temp_filename, mode='w', newline='') as temp_file:
            dict_writer = csv.DictWriter(temp_file, fieldnames=self.freq_bands)
            dict_writer.writeheader()
            dict_writer.writerow(freq_dict)




class Familiarization(Procedure):

    def __init__(self, startlevel=40, signal_length=1):
        """familiarization process

        Args:
            startlevel (int, optional): starting level of procedure in dBHL. Defaults to 40.
            signal_length (int, optional): length of played signals in seconds. Defaults to 1.
        """

        super().__init__(startlevel, signal_length)      
        self.fails = 0 # number of times familiarization failed
        self.tempfile = self.create_temp_csv() # create a temporary file to store level at frequencies

    def get_temp_csv_filename(self):
        return self.tempfile

    def familiarize(self):
        """main funtion

        Returns:
            bool: familiarization successfull
        """

        while True:

            self.tone_heard = True

            # first loop (always -20dBHL)
            while self.tone_heard == True:
                self.play_tone()
                
                if self.tone_heard == True:
                    self.level -= 20
                else:
                    self.level += 10
            
            # second loop (always +10dBHL)
            while self.tone_heard == False:
                self.play_tone()

                if self.tone_heard == False:
                    self.level += 10

            # replay tone with same level
            self.play_tone()

            if self.tone_heard == False:
                self.fails += 1
                if self.fails >= 2:
                    print("Familiarization unsuccessful. Please read rules and start again.")
                    return False
                else:
                    self.level = self.startlevel

            else:
                print("Familiarization successful!")
                self.add_to_temp_csv(self.level, '1000', self.tempfile)
                return True




