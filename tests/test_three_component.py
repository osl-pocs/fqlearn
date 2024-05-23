from unittest import skip

from fqlearn import ThreeComponent

model = ThreeComponent()

scale = 100

def test_add_point():   
    expect_points = model.add_point([(0.2, 0.3, 0.5), (0.1, 0.6, 0.3), (0.4, 0.2, 0.4)])
    expect_one_point = model.add_point([(0.4, 0.1, 0.5)])

    for point in expect_points:
        assert sum(point) == scale

    for point in expect_one_point:
        assert sum(point) == scale

    model.plot()
    
def test_add_eq_line():    
    model.add_eq_line(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], 
                  left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])
    expect_right_eq_line = [(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)]
    expect_left_eq_line = [(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)]

    assert model.right_eq_line == model.sort_points(expect_right_eq_line)
    assert model.left_eq_line == model.sort_points(expect_left_eq_line)

@skip("Check scale and order")
def test_composition_line():
    model.composition_line(left_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], 
                       right_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])
    expect_left_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)]
    expect_right_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)]

    assert model.left_eq_line == model.sort_points(expect_left_eq_line)
    
    xyz = [(x, y, z) for x, y, z in model.add_point(expect_right_eq_line)]
    sorted_right_eq_line = sorted(xyz, key=lambda m: m[0], reverse=True)

    assert model.right_eq_line == sorted_right_eq_line

# def test_eq_slope():
# expect_eq_slope = model.eq_slope(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

#     for point in expect_eq_slope:
#         assert sum(point) == scale

@skip("Check this failing test")
def test_min_diff():
    expect_min_diff = model.min_diff(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

    for point in expect_min_diff:
        assert sum(point) == scale

@skip("Check this failing test")
def test_div_half():
    expect_div_half = model.div_half(right_eq_line=[(0.05, 0.05, 0.9), (0.1, 0.1, 0.8), (0.15, 0.15, 0.7)], left_eq_line=[(0.9, 0.05, 0.05), (0.8, 0.1, 0.1), (0.7, 0.15, 0.15)])

    for point in expect_div_half:
        assert sum(point) == scale
