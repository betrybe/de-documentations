# DE Documentations

A repo to store Data Engineering Frameworks documentation.

## Table of Contents

- [Developing and Testing](#developing-and-testing)
  - [Useful Commands](#useful-commands)
- [Built With](#built-with)

## Developing and Testing

It's best to use a virtual environment to test and develop new features. We recommend `pyenv` or `conda`:
- [pyenv](https://github.com/pyenv/pyenv)
- [conda](https://docs.conda.io/en/latest/)

Having one of these installed makes the developing process easier, helping the user with depency management.

If you need to add a new dependency, make sure to add it to the corresponding `requirements` file:
- `requirements.txt`: General project dependencies. Anything that the main version needs must be added here.
- `requirements.dev.txt`: Dependencies needed for project development.
- `requirements.lint.txt`: Lint dependencies, `flake8` for example.
- `requirements.test.txt`: Dependencies needed for the testing phase.

### Useful Commands

After the initial steps, you can use some useful commands to help your developing process:

1. **Requirements:**
  - `make requirements`: installs all packages from all requirements files
  - `make requirements-dev`: installs all packages from `requirements.dev.txt` file
  - `make requirements-lint`: installs all packages from `requirements.lint.txt` file
  - `make requirements-tests`: installs all packages from `requirements.tests.txt` file
2. **Lint:**
  - `make checks`: runs `black` and `flake8`
  - `make black`: runs only the `black` reformating process
  - `make flake8`: runs only the `flake8` lint process
3. **Tests:**
  - `make tests`: runs `pytest` with coverage

## Built With

- [Python](https://www.python.org/) - Programming language.
- [Flake8](https://pypi.org/project/flake8/) - Lint tool.
- [Black](https://black.readthedocs.io/en/stable/) - Python code formater.
- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - A command-line utility that creates Python projects using templates.