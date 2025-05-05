from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "mlops",
    version = "0.1",
    author = "Sampreeth",
    description= "MLops project",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = ">=3.7",
)