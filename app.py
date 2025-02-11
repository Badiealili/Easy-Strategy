import tkinter as tk
from tkinter import messagebox, filedialog
from robot import Robot
from canvas import Canvas
from frame import Frame

class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.commands = []

    def set_widgets(self, robot: Robot, canvas: Canvas, frame: Frame) -> None:
        """Set the different widgets for the app."""
        self.robot = robot
        self.canvas = canvas
        self.frame = frame
        self.history = [{"position": (self.robot.starting_pos[0],self.robot.starting_pos[1]), "angle": self.robot.starting_angle, "line_id": 0}]

    
    def create_status_window(self) -> None:
        self.status_window = tk.Toplevel(self.root)
        self.status_window.title("Robot Status")
        self.status_window.geometry("300x100")
        self.status_window.angle_label = tk.Label(self.status_window, text=f"Angle: {self.robot.angle}")
        self.status_window.angle_label.pack(pady=10)
        self.status_window.position_label = tk.Label(self.status_window, text=f"position: {(self.robot.x, self.robot.y)}")
        self.status_window.position_label.pack(pady=10)

    def update_status_window(self) -> None:
        self.status_window.angle_label.config(text=f"Angle: {self.robot.angle}")
        self.status_window.position_label.config(text=f"Position: {(self.robot.x, self.robot.y)}")

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
            last = self.history[len(self.history)-1]
            self.canvas._canvas.delete(item["line_id"])
            self.robot.update(last["position"][0], last["position"][1], last["angle"])
            self.update_status_window()


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

        


