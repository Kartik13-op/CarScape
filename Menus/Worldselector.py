import tkinter as tk

class WorldSelector:
    """Displays world selection and police speed setting."""
    def __init__(self, start_game_callback):
        self.start_game_callback = start_game_callback
        self.police_speed = 3.5 # Initial default
        
        self.world_window = tk.Tk()
        self.setup_ui()
        self.world_window.mainloop()

    def setup_ui(self):
        self.world_window.title("Select World Type")
        self.world_window.geometry("800x450")
        self.world_window.configure(bg="#1B1B2F")

        tk.Label(self.world_window, text="Select World Type", font=("Impact", 28), fg="cyan", bg="#1B1B2F").pack(pady=20)

        # Label for slider
        tk.Label(self.world_window, text="Police Speed", font=("Arial", 14), fg="white", bg="#1B1B2F").pack(pady=5)

        # Create slider (Scale widget)
        self.speed_slider = tk.Scale(self.world_window, from_=3.5, to=3.8, resolution=0.01, orient=tk.HORIZONTAL,
                                length=300, bg="#1B1B2F", fg="white", troughcolor="#3FC1C9",
                                highlightbackground="#1B1B2F")
        self.speed_slider.set(self.police_speed)
        self.speed_slider.pack(pady=10)

        def start_selected_world(world_type):
            self.police_speed = self.speed_slider.get()
            self.world_window.destroy()
            # Pass selected settings back to MainGame
            self.start_game_callback(world_type, self.police_speed)

        tk.Button(self.world_window, text="🌍 Normal World", font=("Arial", 14), bg="#3FC1C9", fg="black", width=20,
                command=lambda: start_selected_world('normal')).pack(pady=10)

        tk.Button(self.world_window, text="🟦 Retro World", font=("Arial", 14), bg="#FC5185", fg="white", width=20,
                command=lambda: start_selected_world('retro')).pack(pady=10)

        tk.Button(self.world_window, text="🌑 Hybrid Dark World", font=("Arial", 14), bg="#364F6B", fg="white", width=20,
                command=lambda: start_selected_world('hybrid')).pack(pady=10)
