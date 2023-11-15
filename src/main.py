from fqlearn import McCabeThiele

model = McCabeThiele()
model.set_data(compound_a="methanol", compound_b="water")
# model.set_compositions(xF=0.5, xD=0.94, xW=0.05)
model.set_feed(q = 0.5, xF = 0.5)
# model.solve()
model.fit(xF=0.5, xD=0.94, xW=0.05)  # eliminar
# model.steps()
model.describe()
model.plot()
