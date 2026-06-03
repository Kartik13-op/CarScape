import tkinter as tk

class GameOverMenu:
    """Displays the game over screen and restart/quit options."""
    def __init__(self, final_time, restart_callback, quit_callback):
        self.final_time = final_time
        self.restart_callback = restart_callback
        self.quit_callback = quit_callback

        self.root = tk.Tk()
        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        self.root.title("Game Over - Car-scape")
        self.root.geometry("600x400")
        self.root.configure(bg="#0B132B")

        tk.Label(self.root, text="Game Over!", font=("Impact", 38), fg="red", bg="#0B132B").pack(pady=30)
        tk.Label(self.root, text=f"You were caught!\nTime Survived: {self.final_time:.2f} seconds", font=("Arial", 16), fg="white", bg="#0B132B").pack(pady=20)

        def restart():
            self.root.destroy()
            self.restart_callback()

        def quit_game():
            self.root.destroy()
            self.quit_callback()

        tk.Button(self.root, text="⟳ Restart", font=("Arial", 16, "bold"), bg="orange", fg="white", padx=20, pady=10, command=restart).pack(pady=10)
        tk.Button(self.root, text="❌ Exit", font=("Arial", 14), bg="darkred", fg="white", padx=20, pady=10, command=quit_game).pack(pady=10)
