import tkinter as tk
from tkinter import messagebox, filedialog
from robot import Robot
from canvas import Canvas
from frame import Frame

class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.commands = []
        self.history = [{"position": (0,0), "angle": 0, "line_id": 0}]

    def set_widgets(self, robot: Robot, canvas: Canvas, frame: Frame):
        """Set the different widgets for the app."""
        self.robot = robot
        self.canvas = canvas
        self.frame = frame

    def start(self) -> None:
        """Start the main loop of the tkinter app."""
        self.root.mainloop()

    def reset(self) -> None:
        """Clear the canvas and reset the app and robot attributes to their initial settings."""
        self.history = []
        self.commands = []
        self.canvas.clear()
        self.robot.reset()

    def add_command(self, command: str) -> None:
        """Manually add a command."""
        self.commands.append(command)

    def undo(self):
        if len(self.history) > 1:
            item = self.history.pop()
            self.canvas._canvas.delete(item["line_id"])
            self.robot.update(self.history[len(self.history)-1]["position"][0], self.history[len(self.history)-1]["position"][1], item["angle"])

    def clean_commands(self) -> None:
        """Clean the commands array before saving it to file."""
        ...
    
    def save_commands(self) -> None:
        """Save the command list to a file."""
        if not self.commands:
            messagebox.showwarning("No Commands", "No commands to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "w") as f:
            for command in self.commands:
                f.write(command + "\n")

        messagebox.showinfo("Success", "Commands saved successfully.")

    def update_history(self, entry: dict) -> None:
        """Update the history array with a new entry."""
        self.history.append(entry)

        


