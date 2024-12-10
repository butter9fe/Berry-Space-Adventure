### Imports
# Modules
import sys
import tkinter as tk
from tkinter import ttk, Label
from PIL import Image, ImageTk
from utils.soundthreadmanager import sound_thread
# Tbh idk how u wanna do this this is just placeholder feel free to refactor this or even delete this file lol
# Call for this is under gameobject_player.py, under collision_response() and spaceship

# You can check for self.game.curr_level to display different dialogues based on what level you are on
class Dialogue_Lose:
    def __init__(self, game):
        self.game=game
        self.show_gif_1()


    def show_gif_1(self):
        window2 = Launch("assets\dialog\BSO_GO_GameOver.gif", 1920,1080 ,duration=5000,next_window=self.show_gif_18)
        window2.show()
        sound_thread.play_bgm("./assets/sounds/bgm/game_station_3.wav") #Play sfx: Start game press
    
    def show_gif_18(self):
        window2 = Launch("assets\dialog\BSO_MG_EndThankYou.gif", 1920,1080 ,duration=5000,next_window=lambda:sys.exit())
        window2.show()
    

class Launch:
    def __init__(self, image_path,window_x=480,window_y=270, duration=3000, next_window=None):
        # Create the main window
        self.root = tk.Toplevel()
        
        # Store the callback for next window
        self.next_window = next_window
        
        # Remove window border and make transparent
        self.root.overrideredirect(True)
        self.root.configure(bg='black')  # Set to black for better blending
        self.root.attributes('-transparentcolor', 'black')  # Make black background transparent
        
        # Fixed window size
        self.window_width = window_x
        self.window_height = window_y
        
        # Create frame with transparent background
        self.frame = tk.Frame(
            self.root, 
            bg='black',  # Match the transparent color
            bd=0, 
            highlightthickness=0
        )
        self.frame.pack(fill='both', expand=True)
        
        # Load and prepare the image
        self.original_image = Image.open(image_path)
        
        # Check if image is animated GIF
        self.is_animated = hasattr(self.original_image, 'n_frames') and self.original_image.n_frames > 1
        
        if self.is_animated:
            # For animated GIFs
            self.current_frame = 0
            self.frames = []
            try:
                while True:
                    frame = self.original_image.copy()
                    frame = frame.resize((self.window_width, self.window_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(frame)
                    self.frames.append({
                        'image': photo,
                        'delay': self.original_image.info.get('duration', 100)
                    })
                    self.original_image.seek(self.original_image.tell() + 1)
            except EOFError:
                pass
            
            # Create label with first frame
            self.label = Label(
                self.frame,
                image=self.frames[0]['image'],
                bd=0,
                highlightthickness=0,
                bg='black'  # Match the transparent color
            )
            
            # Start animation
            self.animate()
        else:
            # For static images
            resized_image = self.original_image.resize((self.window_width, self.window_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized_image)
            self.label = Label(
                self.frame,
                image=self.photo,
                bd=0,
                highlightthickness=0,
                bg='black'  # Match the transparent color
            )
        
        # Place the label precisely
        self.label.place(x=0, y=0, width=self.window_width, height=self.window_height)
        
        # Center window on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # Bind escape key to close window
        self.root.bind('<Escape>', lambda e: self.close_window())
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Schedule window closure
        self.root.after(duration, self.close_window)
    
    def animate(self):
        if self.is_animated:
            self.label.configure(image=self.frames[self.current_frame]['image'])
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.root.after(self.frames[self.current_frame]['delay'], self.animate)
    
    def close_window(self):
        self.root.destroy()
        if self.next_window:
            self.next_window()
    
    def show(self):
        self.root.mainloop()

