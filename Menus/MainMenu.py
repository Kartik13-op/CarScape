import tkinter as tk

class MainMenu:
    """Displays the main menu and triggers the world selector."""
    def __init__(self, next_callback):
        self.next_callback = next_callback
        self.root = tk.Tk()
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("CarScape")
        self.root.geometry("800x450")
        self.root.configure(bg="#1a1a1a")

        # Title at top center
        tk.Label(
            self.root,
            text="CarScape",
            font=("Segoe UI", 60, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=(50, 0))

        # Function for start button
        def open_world_selector():
            self.root.destroy()
            self.next_callback()

        # Bottom frame for buttons (sticks to bottom)
        bottom_frame = tk.Frame(self.root, bg="#1a1a1a")
        bottom_frame.pack(side="bottom", fill="x", pady=18)

        # Sub-frame to center both buttons horizontally
        button_frame = tk.Frame(bottom_frame, bg="#1a1a1a")
        button_frame.pack(anchor="center")

        # Start button
        start_btn = tk.Button(
            button_frame,
            text="Start",
            font=("Segoe UI", 14, "bold"),
            bg="#C8FF73",
            fg="black",
            activebackground="#b4ff5a",
            activeforeground="black",
            width=30,
            relief="flat",
            command=open_world_selector
        )
        start_btn.grid(row=0, column=0, padx=(0, 4))

        # Info button (inactive)
        info_btn = tk.Button(
            button_frame,
            text="Info",
            font=("Segoe UI", 10, "bold"),
            bg="#555",
            fg="white",
            width=10,
            relief="flat",
            activebackground="#666"
        )
        info_btn.grid(row=0, column=1)

        # Optional short tagline under title
        tk.Label(
            self.root,
            text="Escape the chase — Drive endlessly!",
            font=("Arial", 26),
            fg="#aaaaaa",
            bg="#1a1a1a"
        ).pack(pady=(10, 10))
