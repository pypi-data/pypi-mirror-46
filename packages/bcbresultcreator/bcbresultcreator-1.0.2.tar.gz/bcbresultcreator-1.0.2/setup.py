import setuptools
from pathlib import Path

setuptools.setup(
    name="bcbresultcreator",
    version="1.0.2",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=[".vscode"])
)
