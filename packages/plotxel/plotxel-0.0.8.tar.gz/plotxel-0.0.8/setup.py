import setuptools
import plotxel

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotxel",
    version=plotxel.__version__,
    author="Daniel Hitchcock",
    author_email="daniel.s.hitchcock@gmail.com",
    description="A wordy but intuitive plotting library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danhitchcock/plotxel",
    packages=setuptools.find_packages(),
    install_requires=['svgwrite', 'cairosvg', 'Pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)