from fqlearn import McCabeThiele

model = McCabeThiele()
model.set_data(compound_a="hexano", compound_b="xileno")
model.fit(xF=0.5, xD=0.94, xW=0.05)
model.plot()
