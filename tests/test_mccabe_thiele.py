from fqlearn import McCabeThiele


def test_binary():
    modelo = McCabeThiele()
    modelo.set_data("methanol", "water")
    assert modelo.compound_a == "methanol"
