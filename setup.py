from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().strip().splitlines()


setup(
    name="chainy",
    version="0.1.0-dev2",
    description="Declarative prompt chaining",
    author="Lucas Lofaro",
    author_email="lucasmlofaro@gmail.com",
    url="https://github.com/FyZyX/chainy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml~=6.0",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
)
