"""Setup script."""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name="koala2",

        version="0.0.33",

        author="Ants, open innovation lab",
        author_email="contact@weareants.fr",

        packages=find_packages(),

        include_package_data=True,

        url="https://github.com/anthill/koala",

        license="GNU GPL3",
        description="Convert Excel document in actionnable python",
        install_requires=[
            'networkx >= 2.1',
            'openpyxl >= 2.5.3',
            'numpy >= 1.14.2',
            'Cython >= 0.28.2',
            'lxml >= 4.1.1',
            'six >= 1.11.0',
        ]
    )
