from setuptools import setup, find_packages
from pathlib import Path

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="nifti2png",
    version="0.0.1",
    url="https://github.com/joshy/nifti2png.git",
    author="Joshy Cyriac",
    author_email="j.cyriac@gmail.com",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ],
    license="BSD-3-Clause",
    description="Converts nifti to png, _not_ a general purpose converter",
    packages=find_packages(),
    install_requires=["tqdm>=4.24"],
    keywords=["nifti", "png"],
    entry_points={"console_scripts": ["nifti2png = nifti2png.__main__:main"]},
)
