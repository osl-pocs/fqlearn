from fqlearn import ThreeComponent

model = ThreeComponent()

def test_add_point():
    expect_points = model.add_point([(20, 30, 50), (10, 60, 30), (40, 20, 40)])
    expect_points = model.add_point((40, 10, 50))
    
    for point in expect_points:
        assert sum(point) == 100

    model.plot()
    
def test_eq_line():
    expect_eq_line = model.eq_line([(10, 40, 50), (30, 60, 10), (50, 20, 30)])
    
    for point in expect_eq_line:
        assert sum(point) == 100

def test_solute_points():
    expect_solute_points = model.solute_points(soluteA=[(5, 5, 90), (10, 10, 80), (15, 15, 70)], soluteB=[(90, 5, 5), (80, 10, 10), (70, 15, 15)])

    for point in expect_solute_points:
        assert sum(point) == 100
