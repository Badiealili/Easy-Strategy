from __future__ import annotations
import canvas
import math

class Robot:
    def __init__(self, canvas: canvas.Canvas, starting_pos: tuple[int, int], starting_angle: int, width: int, height: int) -> None:
        """Class representing the robot itself, used mainly to track its position and angle and to visualise it in the canvas"""
        # Initial attributes
        self.starting_pos = starting_pos
        self.starting_angle = starting_angle
        self.x = starting_pos[0]
        self.y = starting_pos[1]
        self.angle = starting_angle
        self.width = width
        self.height = height
        self.canvas = canvas
        self.shapes = []
        self.update(self.x, self.y, self.angle)

    def update(self, x: int, y: int, angle: int) -> None:
        """Update the robot position and angle with the given parameters.
        Delete the last rendered robot from the canvas and draw a new one on the new position
        """        
        self.x = x
        self.y = y
        self.angle = angle
        for shape in self.shapes:
            self.canvas._canvas.delete(shape)
        # TODO: Recreate the shape to accurately represent the robot and represent its direction
        # x coordinates of the robot polygon
        x1 = self.x - self.width // 2
        x2 = self.x + self.width // 2
        x3 = x2
        x4 = x1
        # y coordinates of the robot polygon
        y1 = self.y - self.height // 2
        y2 = y1
        y3 = self.y + self.height // 2
        y4 = y3

        # Rotated points
        rotated_points = self.rotate(angle=angle, coords=[x1, y1, x2, y2, x3, y3, x4, y4])
        [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rotated_points
        self.shapes.append(self.canvas._canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill="green"))
        # Repeat the same operation but for the robot's arm:
        # x coordinates of the robot arm polygon
        x1 = self.x + 0.25*self.width
        x2 = self.x + self.width // 2
        x3 = x2
        x4 = x1
        
        # y coordinates of the robot arm polygon
        y1 = self.y - self.height // 2
        y2 = y1
        y3 = self.y + self.height // 2
        y4 = y3

        # Rotated points
        rotated_points = self.rotate(angle=angle, coords=[x1, y1, x2, y2, x3, y3, x4, y4])
        [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] = rotated_points
        self.shapes.append(self.canvas._canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill="blue"))

    def reset(self) -> None:
        """Reset the robot to its initial parameters."""
        self.update(self.starting_pos[0], self.starting_pos[1], self.starting_angle)

    def rotate_point(self, x: int, y: int, angle: int, cx: int, cy: int) -> tuple[float, float]:
        """Rotate a specific point (x,y) with an angle 'angle' around the center (cx,cy)"""
        xt = x - cx
        yt = y - cy

        theta = math.radians(angle % 360)
        xr = xt*math.cos(theta) - yt*math.sin(theta)
        yr = xt*math.sin(theta) + yt*math.cos(theta)

        return xr + cx, yr + cy

    def rotate(self, angle: int, coords: tuple[int, int]) -> list[tuple[int, int]]:
        """Rotate the robot rectangle with *angle* degrees around the robot's center point"""
        [x1, y1, x2, y2, x3, y3, x4, y4] = coords
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        new_points = [self.rotate_point(x=x, y=y, angle=angle, cx=self.x, cy=self.y) for x,y in points]
        return new_points


        


