from setuptools import setup, find_packages

with open("README.md") as description_file:
    readme = description_file.read()

with open("requirements.txt") as requirements_file:
    requirements = [line for line in requirements_file]

setup(
    name="documentation",
    version="0.1.0",
    author="data_engineering",
    python_requires=">=3.8.2",
    description="Stores Data Engineering frameworks documentation",
    long_description=readme,
    url="https://github.com/betrybe/docs_framework",
    install_requires=requirements,
    packages=find_packages(),
)
