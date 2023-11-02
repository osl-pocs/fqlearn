# OpenThemoPy

This Project aims to facilitate the teaching of unit operations and thermodynamics. Designed in python, it intends to be a library that uses graphical methods and that applies modern equations solve problems related.

## Features

Now this repo has a module to graph an example for McCabeThiele solution to binary destilation

## Example

```python
from fqlearn import McCabeThiele

model = McCabeThiele()
model.set_data(compound_a="methanol", compound_b="water")
model.fit(xF=0.5, xD=0.94, xW=0.05)
model.plot()
```

![mccabe thiele](docs/dest.png)

## Contributing

We welcome contributions from the community. If you'd like to contribute to this project, please follow these guidelines:

- Fork the repository.
- Create a new branch for your feature or bug fix: `git checkout -b feature-name`
- Commit your changes and provide descriptive commit messages.
- Push your branch to your fork: `git push origin feature-name`
- Create a Pull Request to the `main` branch of the original repository.

## License

This project is licensed under the [CC-BY-4.0](./LICENSE.md).

## Credits

This package was created with
[scicookie](https://github.com/osl-incubator/scicookie) project template.
