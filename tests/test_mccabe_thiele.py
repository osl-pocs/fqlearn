from fqlearn import McCabeThiele


def test_binary():
    model = McCabeThiele()
    model.set_data("methanol", "water")
    assert model.compound_a == "methanol"
