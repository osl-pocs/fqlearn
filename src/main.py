from fqlearn import McCabeThiele

model = McCabeThiele()

model.set_data(compound_a="compuestoA", compound_b="compuestoB")
model.set_compositions(xD=0.94, xW=0.05)
model.set_feed(q=0.5, xF=0.5)
model.solve()
model.describe()
model.plot()

"""model2 = McCabeThiele()
model2.set_data(compound_a='methanol', compound_b='water')
model2.set_compositions(xD=0.94, xW=0.05)
model2.set_feed(q=0.5, xF=0.5)
model2.solve()
model2.describe()
model2.plot()"""
