# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at [github:fqlearn/issues](https://github.com/osl-pocs/fqlearn/issues).

If you are reporting a bug, please include:

  - Your operating system name and version.
  - Any details about your local setup that might be helpful in
    troubleshooting.
  - Detailed steps to reproduce the bug.



### Submit Feedback

The best way to send feedback is to file an issue at
[github:fqlearn/issues](https://github.com/osl-pocs/fqlearn/issues).

If you are proposing a feature:

  - Explain in detail how it would work.
  - Keep the scope as narrow as possible, to make it easier to
    implement.
  - Remember that this is a volunteer-driven project, and that
    contributions are welcome :)

## Get Started!

For development, we encourage you to use `conda`. If you don't know
what is that, check these links:

* https://docs.conda.io/en/latest/

We recommend you to use mamba-forge, a combination of
miniconda + conda-forge + mamba. You can download it from here:
https://github.com/conda-forge/miniforge#mambaforge

Ready to contribute? Here’s how to set up fqlearn for local development.

1. Clone this repository locally:
```bash
$ git clone git@github.com:osl-pocs/fqlearn.git
```
2. Create a conda environment and activate it:
```bash
$ cd fqlearn
$ mamba env create --file conda/base.yaml
```
and
```bash
$ conda activate fqlearn
```
3. Install your local project copy into your conda environment:
```bash
$ poetry install
```
4. Create a branch for local development:
```bash
$ git checkout -b name-of-your-bugfix-or-feature
```
5. When you’re done making changes, check that your changes pass flake8
    and the tests, including testing other Python versions with tox:
```bash
$ pytest
```
6. Commit your changes and push your branch to GitHub:
```bash
$ git add .
$ git commit -m "Your detailed description of your changes."
$ git push origin name-of-your-bugfix-or-feature
```
7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
    Put your new functionality into a function with a docstring, and add
    the feature to the list in README.rst.
3.  The pull request should work for Python == 3.10

## Tips

### Commit message format

**semantic-release** uses the commit messages to determine the consumer
impact of changes in the codebase. Following formalized conventions for
commit messages, **semantic-release** automatically determines the next
[semantic version](https://semver.org) number, generates a changelog and
publishes the release.

By default, **semantic-release** uses [Angular Commit Message
Conventions](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format).
The commit message format can be changed with the `preset` or `config`
options\_ of the
[@semantic-release/commit-analyzer](https://github.com/semantic-release/commit-analyzer#options)
and
[@semantic-release/release-notes-generator](https://github.com/semantic-release/release-notes-generator#options)
plugins.

Tools such as [commitizen](https://github.com/commitizen/cz-cli) or
[commitlint](https://github.com/conventional-changelog/commitlint) can
be used to help contributors and enforce valid commit messages.

The table below shows which commit message gets you which release type
when `semantic-release` runs (using the default configuration):

| Commit message                                                 | Release type     |
|----------------------------------------------------------------|------------------|
| `fix(pencil): stop graphite breaking when pressure is applied` | Fix Release      |
| `feat(pencil): add 'graphiteWidth' option`                     | Feature Release  |
| `perf(pencil): remove graphiteWidth option`                    | Chore            |
| `fix!: The graphiteWidth option has been removed`              | Breaking Release |

source:
<https://github.com/semantic-release/semantic-release/blob/master/README.md#commit-message-format>

As this project uses the `squash and merge` strategy, ensure to apply
the commit message format to the PR's title.
