import setuptools 
setuptools.setup(
    name="Zorigoo",
    version="1.0.0",
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=[".vscode"])
)