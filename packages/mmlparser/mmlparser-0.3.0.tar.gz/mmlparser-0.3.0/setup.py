import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmlparser",
    version="0.3.0",
    author="Chaiporn Jaikaeo",
    author_email="chaiporn.j@ku.ac.th",
    description="MML (Music Macro Language) parser and player for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cjaikaeo/mmlparser-python",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
    ],
)
