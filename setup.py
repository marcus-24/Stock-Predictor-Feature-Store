import os
from setuptools import setup


def read(fname: str) -> str:
    """Reads README file
    Args:
        fname (str): path to readme file
    Returns:
        str: contents in readme
    """
    full_path = os.path.join(os.path.dirname(__file__), fname)
    with open(full_path, encoding="utf-8") as file:
        return file.read()


setup(
    name="Stock-Predictor-Feature-Store",
    version="0.0.1",
    author="Marcus Allen",
    author_email="marcusCallen24@gmail.com",
    url="https://github.com/marcus-24/Stock-Predictor-Feature-Store",
    long_description=read("README.md"),
    packages=["mytools"],
    package_dir={"mytools": "./mytools"},
    py_modules=[],
)
