import tkinter as tk
from app import App
from robot import Robot
from canvas import Canvas
from frame import Frame

# Constants
GRID_SIZE = 1  # 10 mm per grid square
CANVAS_WIDTH =  900 # mm
CANVAS_HEIGHT = 600  # mm

ROBOT_HEIGHT = 40
ROBOT_WIDTH = 30
ROBOT_STARTING_POS = (30,30)
ROBOT_STARTING_ANGLE = 0

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
    app.start()

if __name__ == "__main__":
    main()