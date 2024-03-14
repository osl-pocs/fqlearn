import matplotlib
import ternary

# Make images higher resolution and set default size
matplotlib.rcParams["figure.dpi"] = 200
matplotlib.rcParams["figure.figsize"] = (4, 4)


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
        self._right_equilibrium_line = []
        self._left_equilibrium_line = []
    
    # To add points to the plot   
    def add_point(self, points):
        # Check if points is a list of lists or a single list
        if isinstance(
            points[0], (int, float)
        ):  # Check if the first element of points is a number
            assert points[0] + points[1] + points[2] == self.scale
            self.points.append(points)
        else:
            # If points is a list of lists
            for point in points:
                assert point[0] + point[1] + point[2] == self.scale
                self.points.append(point)
        self.tax.scatter(self.points, marker='s', color='blue')
        return self.points

    # To plot equilibrium line joining the points
    def eq_line(self, points):
        self.add_point(points)
        self.tax.plot(points, linewidth=2.0, label="Equilibrium line")
        self.tax.legend()
        self.tax.show()
        return self.points

    # Join the corresponding points of 2 solutes
    def solute_points(self, soluteA, soluteB):
        for i in range(len(soluteA)):
            pointA = soluteA[i]
            pointB = soluteB[i]
            # Extract x and y coordinates of each point
            xA, yA, zA = pointA
            xB, yB, zB = pointB
            # Plot a line connecting the two points
            self.tax.plot([(xA, yA, zA), (xB, yB, zB)], linewidth=1.0, color='green')
        i + 1
        self.tax.show()            

    # To generate the plot
    def plot(self):
        self.tax.clear_matplotlib_ticks()
        self.tax.get_axes().axis("off")

        ternary.plt.show()
