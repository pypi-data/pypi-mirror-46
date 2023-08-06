from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read()

setup(
    name="cavitometer-deconvolve",
    version="0.0.1",
    author="Bruno Lebon",
    author_email="Bruno.Lebon@brunel.ac.uk",
    description="Hydrophone voltage to pressure conversion",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/blebon/cavitometer-deconvolve",
    install_requires=requirements,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)