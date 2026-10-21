import tkinter as tk
import platform
import subprocess

# Load Windows-specific power management library
if platform.system() == "Windows":
    import ctypes
    ES_CONTINUOUS = 0x80000000
    ES_DISPLAY_REQUIRED = 0x00000002

class EnergyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy")
        self.root.geometry("280x380")
        self.root.configure(bg="#0F0F11") # Deep sleek background
        self.root.attributes('-topmost', True) # Keep above other apps
        self.root.resizable(False, False)
        
        self.is_active = False
        self.mac_process = None
        
        # App Title
        tk.Label(
            root, text="E N E R G Y", font=("Segoe UI Black", 28, "bold"), 
            bg="#0F0F11", fg="#FFFFFF"
        ).pack(pady=(25, 5))
        
        # Status Subtitle
        self.status_label = tk.Label(
            root, text="System: NORMAL", font=("Segoe UI", 10, "bold"), 
            bg="#0F0F11", fg="#666666"
        )
        self.status_label.pack()

        # Canvas for the Lightning Bolt
        self.canvas = tk.Canvas(
            root, width=140, height=170, bg="#0F0F11", 
            highlightthickness=0, cursor="hand2"
        )
        self.canvas.pack(pady=20)

        # Vector coordinates for a sleek lightning bolt
        self.bolt_coords = [75, 10, 25, 90, 60, 90, 45, 160, 110, 70, 75, 70]
        
        # Draw the unlit bolt (inactive state)
        self.bolt = self.canvas.create_polygon(
            self.bolt_coords, fill="#252528", outline="#333336", width=2
        )
        
        # Footer Credit
        tk.Label(
            root, text="Made by Paul Joseph Lijjo", font=("Segoe UI", 9), 
            bg="#0F0F11", fg="#555555"
        ).pack(side="bottom", pady=20)

        # Make the bolt clickable
        self.canvas.bind("<Button-1>", self.toggle)
        
    def toggle(self, event=None):
        self.is_active = not self.is_active
        
        if self.is_active:
            # Turn ON: Ignite neon yellow and lock OS screen power
            self.prevent_sleep(True)
            self.canvas.itemconfig(self.bolt, fill="#E5FF00", outline="#FFFFFF")
            self.status_label.config(text="System: AWAKE", fg="#E5FF00")
        else:
            # Turn OFF: Revert to dark and release OS power lock
            self.prevent_sleep(False)
            self.canvas.itemconfig(self.bolt, fill="#252528", outline="#333336")
            self.status_label.config(text="System: NORMAL", fg="#666666")

    def prevent_sleep(self, activate):
        os_name = platform.system()
        
        if os_name == "Windows":
            if activate:
                ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_DISPLAY_REQUIRED)
            else:
                ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
                
        elif os_name == "Darwin":
            if activate:
                self.mac_process = subprocess.Popen(['caffeinate', '-d'])
            else:
                if self.mac_process:
                    self.mac_process.terminate()
                    self.mac_process = None

if __name__ == "__main__":
    root = tk.Tk()
    app = EnergyApp(root)
    root.mainloop()