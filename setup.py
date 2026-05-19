from setuptools import setup, find_packages

setup(
    name="dependency-tool",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pyyaml",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "dependencyTool=src.cli:main"
        ]
    }
)