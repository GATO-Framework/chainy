from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as file:
        return file.read()


setup(
    name="chainy",
    version="0.1.0-dev3",
    description="Declarative prompt chaining",
    author="Lucas Lofaro",
    author_email="lucasmlofaro@gmail.com",
    url="https://github.com/FyZyX/chainy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml~=6.0",
    ],
    license='MIT',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
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
