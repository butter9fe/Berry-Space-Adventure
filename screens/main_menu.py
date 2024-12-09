### Imports
# Modules
import tkinter as tk
from tkinter import Tk, Label
from PIL import Image, ImageTk
from utils.soundthreadmanager import sound_thread

class Launch:
    sound_thread.play_bgm("./assets/sounds/bgm/game_open.wav") #Play Bgm: Opening Theme
    def __init__(self, image_path, duration=4000, next_window=None):
        # Create the main window
        self.root = Tk()
        
        # Store the callback for next window
        self.next_window = next_window
        
        # Remove window border and make transparent
        self.root.overrideredirect(True)
        self.root.configure(bg='black')  # Set to black for better blending
        self.root.attributes('-transparentcolor', 'black')  # Make black background transparent
        
        # Fixed window size
        self.window_width = 480
        self.window_height = 270
        
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

class MainMenu:
    # Define image paths as class variables
    START_BUTTON_PATH = "assets/menu/BSO_Button_Start.png"
    START_BUTTON_HOVER_PATH = "assets/menu/BSO_Button_Start_Hover.png"
    QUIT_BUTTON_PATH = "assets/menu/BSO_Button_Quit.png"
    QUIT_BUTTON_HOVER_PATH = "assets/menu/BSO_Button_Quit_Hover.png"
    TITLE_PATH = "assets/menu/BSO_Title_Logo.png"
    BACKGROUND_PATH = "assets/menu/BSO_Title_BGstarmoon.gif"
    BERRY_PATH = "assets\menu\BSO_Title_FloatBerry.gif"

    def __init__(self):
        # Create the main window
        self.root = Tk()
        
        # Set title and icon
        self.root.iconbitmap('./assets/favicon.ico')
        self.root.title("Launch Berry's Starlight Odyssey!")
        
        # Window dimensions
        self.window_width = 720
        self.window_height = 405
        
        # Configure root window
        self.root.configure(bg='black')
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Load and setup animated background
        self.background_image = Image.open(self.BACKGROUND_PATH)
        self.background_frames = []
        
        try:
            while True:
                frame = self.background_image.copy()
                frame = frame.resize((self.window_width, self.window_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(frame)
                self.background_frames.append({
                    'image': photo,
                    'delay': self.background_image.info.get('duration', 100)
                })
                self.background_image.seek(self.background_image.tell() + 1)
        except EOFError:
            pass

        # Create background on canvas
        self.background_id = self.canvas.create_image(
            self.window_width//2,
            self.window_height//2,
            image=self.background_frames[0]['image']
        )

        # Load and setup Berry animation
        self.berry_image = Image.open(self.BERRY_PATH)
        self.berry_frames = []
        
        try:
            while True:
                frame = self.berry_image.copy()
                berry_width = 320
                berry_height = 180
                frame = frame.resize((berry_width, berry_height), Image.Resampling.LANCZOS)
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                photo = ImageTk.PhotoImage(frame)
                self.berry_frames.append({
                    'image': photo,
                    'delay': self.berry_image.info.get('duration', 100)
                })
                self.berry_image.seek(self.berry_image.tell() + 1)
        except EOFError:
            pass

        # Create Berry animation on canvas
        padding_x = 20
        padding_y = 50
        self.berry_animation_id = self.canvas.create_image(
            padding_x,
            self.window_height - padding_y,
            image=self.berry_frames[0]['image'],
            anchor='sw'
        )
        
        # Initialize frame counter for Berry animation
        self.current_berry_frame = 0
        
        # Load title
        title_width = 480
        title_height = 270
        title_image = Image.open(self.TITLE_PATH)
        title_image = title_image.resize((title_width, title_height), Image.Resampling.LANCZOS)
        self.title_photo = ImageTk.PhotoImage(title_image)
        
        # Create title on canvas
        title_x = self.window_width // 2
        title_y = (title_height // 2)
        self.title_id = self.canvas.create_image(title_x, title_y, image=self.title_photo)
        
        # Button dimensions
        button_width = 194
        button_height = 42
        
        # Load button images
        start_image = Image.open(self.START_BUTTON_PATH)
        start_image = start_image.resize((button_width, button_height), Image.Resampling.LANCZOS)
        self.start_button_photo = ImageTk.PhotoImage(start_image)
        
        start_hover = Image.open(self.START_BUTTON_HOVER_PATH)
        start_hover = start_hover.resize((button_width, button_height), Image.Resampling.LANCZOS)
        self.start_hover_photo = ImageTk.PhotoImage(start_hover)
        
        quit_image = Image.open(self.QUIT_BUTTON_PATH)
        quit_image = quit_image.resize((button_width, button_height), Image.Resampling.LANCZOS)
        self.quit_button_photo = ImageTk.PhotoImage(quit_image)
        
        quit_hover = Image.open(self.QUIT_BUTTON_HOVER_PATH)
        quit_hover = quit_hover.resize((button_width, button_height), Image.Resampling.LANCZOS)
        self.quit_hover_photo = ImageTk.PhotoImage(quit_hover)
        
        # Calculate button positions
        start_y = (self.window_height - (2 * button_height + 20)) // 2 + 50
        quit_y = start_y + button_height + 20
        button_x = self.window_width // 2
        
        # Create buttons on canvas
        self.start_button_id = self.canvas.create_image(
            button_x, start_y + button_height//2,
            image=self.start_button_photo,
            tags=("start_button",)
        )
        
        self.quit_button_id = self.canvas.create_image(
            button_x, quit_y + button_height//2,
            image=self.quit_button_photo,
            tags=("quit_button",)
        )
        
        # Bind canvas events
        self.canvas.tag_bind("start_button", '<Enter>', self.on_start_hover)
        self.canvas.tag_bind("start_button", '<Leave>', self.on_start_leave)
        self.canvas.tag_bind("start_button", '<Button-1>', self.on_start_click)
        self.canvas.tag_bind("quit_button", '<Enter>', self.on_quit_hover)
        self.canvas.tag_bind("quit_button", '<Leave>', self.on_quit_leave)
        self.canvas.tag_bind("quit_button", '<Button-1>', self.on_quit_click)
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        
        # Make window non-resizable
        self.root.resizable(False, False)
        
        # Start background animation
        self.current_background_frame = 0
        self.animate_background()
    
    def animate_background(self):
        self.canvas.itemconfig(self.background_id, image=self.background_frames[self.current_background_frame]['image'])
        self.current_background_frame = (self.current_background_frame + 1) % len(self.background_frames)

        self.canvas.itemconfig(self.berry_animation_id, image=self.berry_frames[self.current_berry_frame]['image'])
        self.current_berry_frame = (self.current_berry_frame + 1) % len(self.berry_frames)
        
        delay = min(self.background_frames[self.current_background_frame]['delay'],
                   self.berry_frames[self.current_berry_frame]['delay'])
        self.root.after(delay, self.animate_background)
    
    def on_start_hover(self, event):
        self.canvas.itemconfig(self.start_button_id, image=self.start_hover_photo)
        sound_thread.play_sfx("./assets/sounds/sfx/menu_button_scrollpass.wav")  #Play sfx: button hover

    def on_start_leave(self, event):
        self.canvas.itemconfig(self.start_button_id, image=self.start_button_photo)
        self.canvas.config(cursor="")
    
    def on_quit_hover(self, event):
        self.canvas.itemconfig(self.quit_button_id, image=self.quit_hover_photo)
        sound_thread.play_sfx("./assets/sounds/sfx/menu_button_scrollpass.wav") #Play sfx: button hover
    
    def on_quit_leave(self, event):
        self.canvas.itemconfig(self.quit_button_id, image=self.quit_button_photo)
        self.canvas.config(cursor="")
    
    def on_start_click(self, event):                
        sound_thread.play_sfx("./assets/sounds/sfx/menu_button_start.wav") #Play sfx: Start game press
        self.root.destroy()
    
    def on_quit_click(self, event):        
        sound_thread.play_sfx("./assets/sounds/sfx/menu_button_quit.wav") #Play sfx: Quit game press
        self.root.quit()
    
    def show(self):
        self.root.mainloop()

def launch_menu():
    menu = MainMenu()
    menu.show() 
    # main menu music 

def show_second_gif():
    window2 = Launch("assets\menu\BSO_MG_StarSysIntro2.gif", duration=4000, next_window=launch_menu)
    window2.show()
    # play like a computer startup sound here

def launch_sequence():
    window1 = Launch("assets\menu\BSO_MG_StarSysIntro1.gif", duration=5000, next_window=show_second_gif)
    window1.show()
    # play like a computer startup sound here
