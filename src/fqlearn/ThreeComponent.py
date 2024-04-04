import matplotlib as plt
import numpy as np
import pandas as pd
import ternary
from scipy.interpolate import CubicSpline

# Make images higher resolution and set default size
plt.rcParams["figure.dpi"] = 200
plt.rcParams["figure.figsize"] = (4, 4)


# This class plots a ternary phase diagrams using triangular axes
class ThreeComponent:
    def __init__(self):
        self.scale = 100
        self.figure, self.tax = ternary.figure(scale=self.scale)
        self.tax.boundary(linewidth=1.5)
        self.tax.gridlines(color="black", multiple=6)
        self.tax.gridlines(color="blue", multiple=2, linewidth=0.5)
        self.fontsize = 8
        # self.tax.ticks(fontsize=5)
        self.offset = 0.14
        self.tax.set_title("Three Component Phase Diagram\n", fontsize=self.fontsize)
        self.tax.left_axis_label(
            "Mass fraction of C", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.right_axis_label(
            "Mass fraction of B", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.bottom_axis_label(
            "Mass fraction of A", fontsize=self.fontsize, offset=self.offset
        )
        self.tax.left_corner_label("C", fontsize=self.fontsize)
        self.tax.right_corner_label("A", fontsize=self.fontsize)
        self.tax.top_corner_label("B", fontsize=self.fontsize)
        self.tax.ticks(axis="lbr", linewidth=1, multiple=10, offset=0.02)

        self.tax.set_background_color(
            color="whitesmoke", alpha=0.7
        )  # the default, essentially

        self.points = []
        self.right_eq_line = []
        self.left_eq_line = []

    # To add points to the plot
    def add_point(self, points):
        # Check if points is an empty list
        if not points:
            raise ValueError("The 'points' list cannot be empty. Please provide valid points.")
    
        # Remove duplicate points
        new_points = list(set(points))

        # Multiply each point by 100
        new_points = [(x * 100, y * 100, z * 100) for x, y, z in new_points]

        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in new_points]
        sorted_points = sorted(xyz, key=lambda m: m[0])

        # Check if the points are in a list of lists or a single list
        if isinstance(
            sorted_points[0], (int, float)
        ):  # Check if the first element of points is a number
            assert sorted_points[0] + sorted_points[1] + sorted_points[2] == self.scale
            self.points.append(sorted_points)
        else:
            # If the points are in a list of lists
            for sorted_point in sorted_points:
                assert sorted_point[0] + sorted_point[1] + sorted_point[2] == self.scale
                self.points.append(sorted_point)
        
        # Plot the points
        self.tax.scatter(
            self.points, linewidth=1.0, marker="o", color="red", label="Points"
        )
        return self.points

    # To plot an equilibrium line joining the points on the right and left
    def eq_line(self, right_eq_line, left_eq_line):
        eq_line = self.add_point(right_eq_line)
        left_eq = self.add_point(left_eq_line)
        eq_line.extend(left_eq)

        # Remove duplicate points
        eq_line_plot = list(set(eq_line))

        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in eq_line_plot]
        sorted_eq = sorted(xyz, key=lambda m: m[0])

        self.tax.plot(sorted_eq, linewidth=1.0, color="blue", label="Equilibrium line")

    # To join the corresponding points of 2 solutes
    def solute_points(self, soluteA, soluteB):
        # Multiply each point by 100
        new_soluteA = [(x * 100, y * 100, z * 100) for x, y, z in soluteA]
        new_soluteB = [(x * 100, y * 100, z * 100) for x, y, z in soluteB]

        # Sort the points in ascending order
        xyz = [(x, y, z) for x, y, z in new_soluteA]
        sorted_soluteA = sorted(xyz, key=lambda m: m[0])
        xyz = [(x, y, z) for x, y, z in new_soluteB]
        sorted_soluteB = sorted(xyz, key=lambda m: m[0], reverse=True)

        for i in range(len(soluteA)):
            pointA = sorted_soluteA[i]
            assert sum(pointA) == self.scale
            pointB = sorted_soluteB[i]
            assert sum(pointB) == self.scale

            # Extract x and y coordinates of each point
            xA, yA, zA = pointA
            xB, yB, zB = pointB
  
            # Plot the two points
            self.tax.scatter(
                [(xA, yA, zA), (xB, yB, zB)], marker="s", color="red")
            # Plot a line connecting the two points
            self.tax.plot(
                [(xA, yA, zA), (xB, yB, zB)],
                linewidth=1.0,
                color="blue",
            )
        i + 1
        self.points.extend(sorted_soluteA)
        self.points.extend(sorted_soluteB)
        return self.points

    # Cubic spline interpolation of the points
    def interpolate(self, points):
        self.add_point(points)

        # Cubic spline interpolation
        x = [x for x, y, z in self.points]
        y = [y for x, y, z in self.points]
        z = [z for x, y, z in self.points]

        f = CubicSpline(x, y, bc_type="natural")
        x_cubic = np.linspace(0, 100, 100)
        y_cubic = f(x_cubic)

        # Remove negative points
        points_to_plot = [
            [i, j]
            for i, j in np.column_stack((x_cubic, y_cubic))
            if 0 <= i <= 100 and 0 <= j <= 100
        ]

        # Plot the curve
        self.tax.plot(points_to_plot, linewidth=1.0, label="Interpolated curve")

    # To generate the plot
    def plot(self):
        self.tax.clear_matplotlib_ticks()
        self.tax.get_axes().axis("off")
        self.tax.legend()
        ternary.plt.show()

model = ThreeComponent()

# points = [(0.02, 0.02, 0.96), (0.025, 0.06, 0.915), (0.03, 0.1, 0.87), 
#             (0.035, 0.16, 0.805), (0.04, 0.2, 0.76), (0.045, 0.25, 0.705), 
#             (0.05, 0.3, 0.65), (0.07, 0.36, 0.57), (0.09, 0.4, 0.51), 
#             (0.14, 0.48, 0.38), (0.33, 0.49, 0.18), (0.97, 0.01, 0.02), 
#             (0.95, 0.03, 0.02), (0.91, 0.06, 0.03), (0.88, 0.09, 0.03), 
#             (0.83, 0.13, 0.04), (0.79, 0.17, 0.04), (0.745, 0.2, 0.055), 
#             (0.68, 0.26, 0.06), (0.62, 0.3, 0.08), (0.49, 0.4, 0.11), 
#             (0.33, 0.49, 0.18)] 

right_eq_line = [(0.02, 0.02, 0.96), (0.025, 0.06, 0.915), (0.03, 0.1, 0.87), 
            (0.035, 0.16, 0.805), (0.04, 0.2, 0.76), (0.045, 0.25, 0.705), 
            (0.05, 0.3, 0.65), (0.07, 0.36, 0.57), (0.09, 0.4, 0.51), 
            (0.14, 0.48, 0.38), (0.33, 0.49, 0.18)]
left_eq_line = [(0.97, 0.01, 0.02), (0.95, 0.03, 0.02), (0.91, 0.06, 0.03), 
                (0.88, 0.09, 0.03), (0.83, 0.13, 0.04), (0.79, 0.17, 0.04), 
                (0.745, 0.2, 0.055), (0.68, 0.26, 0.06), (0.62, 0.3, 0.08), 
                (0.49, 0.4, 0.11), (0.33, 0.49, 0.18)]

# points = []

# model.eq_line(right_eq_line, left_eq_line)
model.solute_points(right_eq_line, left_eq_line)
# model.interpolate(points)
# model.add_point(points)
model.plot()
