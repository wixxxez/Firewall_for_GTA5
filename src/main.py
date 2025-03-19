import keyboard
import tkinter as tk
from src.app.services.FireWallService import Utilities

class HotkeyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotkey Listener App")
        self.root.geometry("400x400")
        self.active = False
        self.hotkey = None
        self.alt_pressed = False
        if Utilities.is_firewall_enabled(): 

             
            # Initialize overlay and set it up
            self.setup_overlay()
            # Add the hotkey entry field
            self.hotkey_var = tk.StringVar()
            self.hotkey_entry = tk.Entry(self.root, textvariable=self.hotkey_var, state="readonly")
            self.hotkey_entry.pack(pady=20)

            
            # Button to start capturing hotkey
            self.capture_button = tk.Button(self.root, text="Capture Hotkey", command=self.start_hotkey_capture)
            self.capture_button.pack(pady=10)

            # self.text_field = tk.Label(self.root, text="Firewall in enabled." )
            # self.text_field.pack(expand=False)

        else: 

            self.text_field = tk.Label(self.root, text="Firewall in disabled. Please enable firewall", fg='red', bg='black' )
            self.text_field.pack(expand=True)

    def setup_overlay(self):
        """ Create the overlay window visible above all applications """
        self.overlay = tk.Toplevel(self.root)
        self.overlay.title("Hotkey Overlay")
        
        # Remove window borders and decorations for overlay
        self.overlay.overrideredirect(True)  # No window border
        self.overlay.attributes('-topmost', True)  # Keep window on top of all others
        self.overlay.attributes('-transparentcolor', 'white')  # Make background transparent

        # Set window size and text label
        self.overlay_label = tk.Label(self.overlay, text="Hotkey: None", bg="lightgrey", font=("Arial", 12), width=20, height=2)
        self.overlay_label.pack(fill="both", expand=True)

        # Place overlay at bottom-right corner of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        overlay_width = self.overlay_label.winfo_reqwidth() + 50
        overlay_height = self.overlay_label.winfo_reqheight()

        # Position the overlay in the bottom-right corner
        self.overlay.geometry(f"{overlay_width}x{overlay_height}+{screen_width - overlay_width - 10}+{screen_height - overlay_height - 10}")
        
        # Ensure overlay is always on top of other windows
        self.overlay.lift()

    def toggle_message(self):
        """ This function will be triggered by the hotkey """
        if Utilities.check_firewall_rule(): 
            self.overlay_label.config(text=f"Hotkey: {self.hotkey}\nFirewall rule is disabled", fg='red', bg='black', font='Roboto')# Update overlay text
            Utilities.remove_firewall_rule()

            
        else: 
            self.overlay_label.config(text=f"Hotkey: {self.hotkey}\nFirewall rule is enabled", fg='green', bg='black', font='Roboto')# Update overlay text
            Utilities.add_firewall_rule()


    def listen_hotkey(self):
        """ Global hotkey listener """
        if self.hotkey:
            keyboard.add_hotkey(self.hotkey, self.toggle_message)
            keyboard.wait()

    def start_hotkey_capture(self):
        """ Capture user-defined Alt + key hotkeys """
        self.hotkey_entry.config(state="normal")
        self.hotkey_entry.delete(0, tk.END)

        # Open a modal to listen for Alt key + another key
        self.capture_window = tk.Toplevel(self.root)
        self.capture_window.title("Capture Hotkey")
        self.capture_window.geometry("250x100")
        
        label = tk.Label(self.capture_window, text="Press Alt + key", font=("Arial", 14))
        label.pack(pady=10)
        
        def detect_key_press(e):
            if e.name == "alt":
                self.alt_pressed = True  # Mark Alt as pressed
            elif self.alt_pressed and e.event_type == "down":
                # Save new hotkey
                new_hotkey = f"alt+{e.name}"
                self.hotkey_var.set(new_hotkey)
                self.hotkey = new_hotkey
                self.hotkey_entry.config(state="readonly")
                
                # Remove previous hotkey and set new one
                keyboard.unhook_all()
                keyboard.add_hotkey(self.hotkey, self.toggle_message)

                # Close capture window
                self.capture_window.destroy()
                self.capture_window = None
                
                self.toggle_message()

                self.alt_pressed = False  # Reset Alt flag
                return True  # Stop capturing

        keyboard.hook(detect_key_press)

if __name__ == "__main__":
    root = tk.Tk()
     
    app = HotkeyApp(root)
    root.mainloop()
