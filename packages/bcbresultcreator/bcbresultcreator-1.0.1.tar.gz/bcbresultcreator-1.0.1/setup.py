import setuptools
from pathlib import Path

setuptools.setup(
    name="bcbresultcreator",
    version="1.0.1",
    long_description=Path("README.md").read_text(),
    packages=["bcb_result", "bcb_result\\bcb_json"]
)
