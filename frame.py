import tkinter as tk

class Frame:
    """Wrapper aronund the tkinter frame class with extra parameters and custom methods"""
    def __init__(self, root: tk.Tk, app) -> None:
        # Initial attributes
        self._frame = tk.Frame(root)
        self.app = app
        
        # Place the canvas on the right side of the window
        self._frame.pack(side=tk.RIGHT)

        # Buttons
        tk.Button(self._frame, text="Save Commands", command=self.app.save_commands).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Clear Canvas", command=self.app.reset).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Baisser La Pince Droite", command=lambda: self.app.add_command("LR")).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Baisser La Pince Gauche", command=lambda: self.app.add_command("LL")).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Baisser Les Deux Pinces", command=lambda: self.app.add_command("LA")).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Lever La Pince Droite", command=lambda: self.app.add_command("HR")).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Lever La Pince Gauche", command=lambda: self.app.add_command("HL")).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Lever Les Deux Pinces", command=lambda: self.app.add_command("HA")).pack(fill=tk.X, pady=5)
        tk.Button(self._frame, text="Ctrl+Z", command=self.app.undo).pack(fill=tk.X, pady=5)

