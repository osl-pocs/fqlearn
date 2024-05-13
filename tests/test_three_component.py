from fqlearn import ThreeComponent

model = ThreeComponent()

def test_add_point():
    expect_points = model.add_point([(0.2, 0.3, 0.5), (0.1, 0.6, 0.3), (0.4, 0.2, 0.4)])
    expect_points = model.add_point((0.4, 0.1, 0.5))
    
    for point in expect_points:
        assert sum(point) == 100

    model.plot()
    
def test_add_eq_line():
    expect_add_eq_line = model.add_eq_line(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])
    
    for point in expect_add_eq_line:
        assert sum(point) == 100

def test_solute_points():
    expect_solute_points = model.solute_points(soluteA=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], soluteB=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

    for point in expect_solute_points:
        assert sum(point) == 100

def test_eq_slope():
    expect_eq_slope = model.eq_slope(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

    for point in expect_eq_slope:
        assert sum(point) == 100

def test_min_diff():
    expect_min_diff = model.min_diff(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

    for point in expect_min_diff:
        assert sum(point) == 100

def test_div_half():
    expect_div_half = model.div_half(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

    for point in expect_div_half:
        assert sum(point) == 100
