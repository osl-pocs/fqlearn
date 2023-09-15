# Transfer mass vizsolver

This Project aims to facilitate the teaching of mass transfer phenomena. Designed in python, it intends to be a library that uses graphical methods and that applies modern equations to predict the behavior of mass transfer.

## Features

Now this repo has a module to graph an example for mcthiele solution to binary destilation

## Example

```python
from fqlearn import McCabeThiele

model = McCabeThiele()
model.set_data(compound_a="methanol", compound_b="water")
model.fit(xF=0.5, xD=0.94, xW=0.05)
model.plot()
```

![mccabe thiele](docs/dest.png)

## Credits

This package was created with
[scicookie](https://github.com/osl-incubator/scicookie) project template.
