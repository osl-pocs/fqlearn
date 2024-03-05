import matplotlib
import ternary

# Make images higher resolution and set default size
matplotlib.rcParams['figure.dpi'] = 200
matplotlib.rcParams['figure.figsize'] = (4, 4)

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
        self.tax.left_axis_label("Mass fraction of C", fontsize=self.fontsize, offset=self.offset)
        self.tax.right_axis_label("Mass fraction of B", fontsize=self.fontsize, offset=self.offset)
        self.tax.bottom_axis_label("Mass fraction of A", fontsize=self.fontsize, offset=self.offset)
        self.tax.left_corner_label("C", fontsize=self.fontsize)
        self.tax.right_corner_label("A", fontsize=self.fontsize)
        self.tax.top_corner_label("B", fontsize=self.fontsize)
        self.tax.ticks(axis='lbr', linewidth=1, multiple=10, offset=0.02)

        self.tax.set_background_color(color="whitesmoke", alpha=0.7) # the default, essentially
       
    def add_points(self, points):
        # Check if points is a list of lists or a single list
        if isinstance(points[0], (int, float)):  # Check if the first element of points is a number
            assert points[0] + points[1] + points[2] == self.scale
            # If points is a single list, convert it to a list of one-element lists
            points = [points]
        else:
            # If points is a list of lists
            for point in points:
                assert point[0] + point[1] + point[2] == self.scale
        self.tax.scatter(points, marker='s', color='blue')
        return points
    
    # To plot equilibrium line
    def eq_line(self, points):
        self.add_points(points)
        self.tax.plot(points, linewidth=2.0, label="Equilibrium line")
        self.tax.legend()
        self.tax.show()

    def plot(self):
        self.tax.clear_matplotlib_ticks()
        self.tax.get_axes().axis('off')

        ternary.plt.show()

model = ThreeComponent()

# To plot points; specify points in the order A,B,C
model.add_points([(20, 50, 30), (30, 60, 10), (70, 10, 20)])

# To plot equilibrium line
eq_points = model.add_points([(20, 50, 30), (30, 60, 10), (70, 10, 20)])
model.eq_line(eq_points)

# To plot points
model.plot()
