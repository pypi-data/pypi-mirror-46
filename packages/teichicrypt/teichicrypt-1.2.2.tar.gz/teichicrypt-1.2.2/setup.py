import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="teichicrypt",
    version="1.2.2",
    author="Teichi",
    author_email="tobias@teichmann.top",
    description="self build crypting algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tobi08151405/crypt",
    packages=setuptools.find_packages(),
    entry_points = {"console_scripts": ["teichicrypt=teichicrypt:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=['mpmath'],
)
