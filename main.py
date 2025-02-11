import tkinter as tk
from app import App
from robot import Robot
from canvas import Canvas
from frame import Frame
from params import *

def main() -> None:
    """Start the main App."""
    root = tk.Tk()
    app = App(root=root)
    canvas = Canvas(root=root, app=app, robot=None, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, grid_size=GRID_SIZE)
    robot = Robot(canvas=canvas, starting_pos=ROBOT_STARTING_POS, starting_angle=ROBOT_STARTING_ANGLE, width=ROBOT_WIDTH, height=ROBOT_HEIGHT)
    canvas.robot = robot
    app.set_widgets(robot=robot, canvas=canvas, frame=None)
    frame = Frame(root, app)
    app.set_widgets(robot=robot, canvas=canvas, frame=frame)
    app.create_status_window()
    app.start()

if __name__ == "__main__":
    main()