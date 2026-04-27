from setuptools import setup, find_packages

setup(
    name="dependency-tool",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "dependencyTool=src.cli:main"
        ]
    }
)