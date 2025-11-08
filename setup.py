from setuptools import setup

setup(
    name="terminal-tetris",
    version="0.2.0",  # Update from 0.1.0 to 0.2.0
    packages=["tetris"],
    package_dir={"": "src"},
    python_requires=">=3.6",
)
