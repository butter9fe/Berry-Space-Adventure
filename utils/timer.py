"""
Centralized frame-by-frame update controller
"""
class Timer():
    """
    Initialises variables
    """
    def __init__(self):
        self.is_running = True
        self.time_scale = 1.0 # For slow-mo later. 1.0 = Real-time. < 1.0 = Slow. > 1.0 = Fast

    """
    Constantly running update function
    """
    def update_timer(self, root, update_function):
        # Parameter checking
        if (not callable(update_function)):
            print("update_function is not a function! Breaking...")
            return
        
        # Start the timer
        if (self.is_running):
            update_function(self.time_scale) # Call function provided in parameter
            root.after(1, lambda: self.update_timer(root, update_function)) # Recursion: Call this function again after main loop is complete

    def update_timescale(self, new_time_scale: float):
        self.time_scale = new_time_scale

    def stop_timer(self):
        self.is_running = False

