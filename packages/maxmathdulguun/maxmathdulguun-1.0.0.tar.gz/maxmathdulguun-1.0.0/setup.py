import setuptools
from pathlib import Path

setuptools.setup(
name="maxmathdulguun",
version="1.0.0", 
long_description=Path("README.md").read_text(),
packages=setuptools.find_packages(exclude=["__pycache__", "lesson17.py"])
)