from __future__ import annotations
import tkinter as tk
import robot
import app
from PIL import Image, ImageTk
import math

class Canvas:
    """Wrapper class around the tkinter canvas class, with extra parameters and custom methods"""
    def __init__(self, root: tk.Tk, app: app.App, robot: robot.Robot, height: int, width: int, grid_size:int) -> None:
        # Initial attributes
        self.app = app
        self.robot = robot
        self.height = height
        self.width =  width
        self.grid_size = grid_size
        self.guidelines = []
        self.valid_line = None
        self._canvas = tk.Canvas(root, height=self.height, width=self.width)
        
        # Place the canvas on the left side of the window
        self._canvas.pack(side=tk.LEFT)

        # Bind mouse events
        self._canvas.bind("<ButtonPress-1>", self.mouse_down)
        self._canvas.bind("<B1-Motion>", self.mouse_drag)
        self._canvas.bind("<ButtonRelease-1>", self.mouse_up)

        # Draw background image (the playmat) and foreground grid to easily trace movements
        self.draw_bg_image("playmat.jpg")
        # self.draw_grid()

    def draw_bg_image(self, img: str) -> None:
        """Add a new background image to the canvas.
        
        Args:
            img (str): Background image file name."""
        self.bg_img = Image.open(img)
        self.bg_img = self.bg_img.resize((self.width, self.height), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self._canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

    def draw_grid(self) -> None:
        """Draws a millimeter grid on the canvas."""
        for x in range(0, self.width, self.grid_size):
            self._canvas.create_line(x, 0, x, self.height, fill="pink")
        for y in range(0, self.height, self.grid_size):
            self._canvas.create_line(0, y, self.width, y, fill="pink")

    def mouse_down(self, event) -> None:
        """Event handler for clicking the mouse on the canvas.
        Starts a new line from the robot position."""
        # Position the valid_line attribute to True if we're starting the line from the robot's current position
        x = (event.x // self.grid_size) * self.grid_size
        y = (event.y // self.grid_size) * self.grid_size
        # Check if the mouse is clicked inside the robot, thus, a valid line is started
        self.valid_line = (x > self.robot.x - self.robot.width and x < self.robot.x + self.robot.width) and (y > self.robot.y - self.robot.height and y < self.robot.y + self.robot.height)
    
    def mouse_drag(self, event) -> None:
        """Event handler for dragging the mouse on the canvas.
        Draws a line that follows the mouse"""
        # Check if the starting position is valid
        if not self.valid_line:
            return
        
        x = (event.x // self.grid_size) * self.grid_size
        y = (event.y // self.grid_size) * self.grid_size
        
        # Delete the last line to create a new one whenever the mouse moves
        for guideline in self.guidelines:
            self._canvas.delete(guideline)
        self.guidelines = []
        self.guidelines.append(self._canvas.create_line(self.robot.x, self.robot.y, x, y, fill="cyan", width=2))
        # Draw the robot stopping limit, takes some calculations.
        y1 = y + ( self.robot.width // 2)
        y2 = y1
        x1 = x - self.robot.height // 2
        x2 = x + self.robot.height // 2

        distance = round(math.sqrt(((self.robot.x - x)**2) + (self.robot.y - y)**2))
        angle_cosine = (x - self.robot.x) / distance
        angle = round(math.degrees(math.acos(angle_cosine)))

        # Correct the value of the angle depending on the direction
        if y < self.robot.y:
            angle = -angle % 360

        # Calculate the rotation
        angle_change = (angle - self.robot.angle)
        # Pick the smallest angle change of the two directions
        if angle_change > 180:
            angle_change = -angle_change % 360
        elif angle_change < - 180:
            angle_change = -(angle_change % 360)
                
        # Inverse the angle to account for the optimazation done by minimizing the rotation angle
        if abs(angle_change) > 90:
            angle = angle + 180
        
        angle-= 90

        x1, y1 = self.rotate_point(x=x1, y=y1, angle=angle, cx=x, cy=y)
        x2, y2 = self.rotate_point(x=x2, y=y2, angle=angle, cx=x, cy=y)
        self.guidelines.append(self._canvas.create_line(x2, y2, x1, y1, fill="yellow", width=2))

    def mouse_up(self, event):
        """Event handler for releasing the mouse on the canvas.
        Ends the drawing of the line"""
        # Check if the drawn line is valid
        if not self.valid_line:
            return
        
        x = (event.x // self.grid_size) * self.grid_size    
        y = (event.y // self.grid_size) * self.grid_size

        distance = round(math.sqrt(((self.robot.x - x)**2) + (self.robot.y - y)**2))
        
        # If there was no displacement, do nothing. 
        if distance == 0:
            return

        # Calculate the new angle based on the drawn trajectory
        angle_cosine = (x - self.robot.x) / distance
        angle = round(math.degrees(math.acos(angle_cosine)))

        # Correct the value of the angle depending on the direction
        if y < self.robot.y:
            angle = -angle % 360

        # Calculate the rotation
        angle_change = angle - self.robot.angle

        # Pick the smallest angle change of the two directions
        if angle_change > 180:
            angle_change = -(360 - angle_change)
        elif angle_change < - 180:
            angle_change = (angle_change % 360)

        commands = []
        if angle_change == 0:
            command = "F" + str(distance)
            commands.append(command)

        elif abs(angle_change) == 180:
            command = "B" + str(distance)
            commands.append(command)

        elif abs(angle_change) <= 90:
            commands.extend(["R" + str(angle_change), "F" + str(distance)])

        # Minimize the rotation degree whenever possible
        # Example: if rotation is 135, instead of rotating 135 degrees and going forward, rotate -45 degrees and go backwards
        # Might change depending on the next action
        else:
            angle_change = angle_change % 360 - 180
            angle = (angle - 180) % 360
            commands.extend(["R" + str(angle_change), "B" + str(distance)])

        # Update everything
        self.robot.update(x=x, y=y, angle=angle)
        self.app.commands.extend(commands)
        self.app.update_history({"position": (self.robot.x, self.robot.y), "angle": self.robot.angle, "line_id": self.guidelines[0]})
        self.app.update_status_window()
        self._canvas.delete(self.guidelines[1])
        self.guidelines = []

    def rotate_point(self, x: int, y: int, angle: int, cx: int, cy: int) -> tuple[float, float]:
        """Rotate a specific point (x,y) with an angle 'angle' around the center (cx,cy)"""
        xt = x - cx
        yt = y - cy

        theta = math.radians(angle % 360)
        xr = xt*math.cos(theta) - yt*math.sin(theta)
        yr = xt*math.sin(theta) + yt*math.cos(theta)

        return xr + cx, yr + cy

    def clear(self):
        """Clear the canvas from the drawn path."""
        self._canvas.delete("all")
        self.draw_bg_image("playmat.jpg")
        # self.draw_grid()
    