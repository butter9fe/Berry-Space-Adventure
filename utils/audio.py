"""
Centralized Audio player
"""
import winsound
import threading
import time

class sounds():

    """
    Initialises variables
    """
    def __init__(self):   
        pass
    """
    Function to play the sound
    """
    def play_sound(self,file_path):
        winsound.PlaySound(file_path, winsound.SND_FILENAME)
    """
    Function to call the play_sound function after delay(s)
    """
    def play_audio(self,file_path, delay=0):
        if delay > 0:
            threading.Thread(target=lambda: time.sleep(delay) or self.play_sound(file_path)).start()
        else:
            threading.Thread(target=lambda: self.play_sound(file_path)).start()


"""
How to Run Aduio Files -SK

1. Aduio Wo interuppting code

from utils.audio import sounds
sounds().play_audio("./assets/sfx/ashcroft_targets.wav", delay=1)

2. Aduio that INTERUPTS code

winsound.PlaySound("Welcome.wav",winsound.SND_FILENAME) #[Finish audio before stop (normal way)]

3. Sys Sounds 

winsound.PlaySound("SystemExit",0) #Exit Game Sound [Finish before continuing code]
"""

#print("Playing the file "+"SystemQuestion")
#winsound.PlaySound("Welcome.wav",winsound.SND_FILENAME) #[Finish audio before stop (normal way)]
#winsound.PlaySound("SystemExit",0) #Exit Game Sound [Finish before continuing code]