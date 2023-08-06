import setuptools
from pathlib import Path

setuptools.setup(
    name="bayaramax", #package_name
    version="1.0.0",
    long_description=Path("README.md").read_text(),
    #long_description="",
    packages=setuptools.find_packages(exclude=[".vscode"])
    )

