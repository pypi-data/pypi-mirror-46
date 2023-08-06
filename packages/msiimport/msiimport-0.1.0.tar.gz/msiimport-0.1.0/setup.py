from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    version="0.1.0",
    name="msiimport",
    description="Access analyze75 formatted mass spec images",
    author="Jade Bilkey",
    author_email="python@thefumon.com",
    long_description_content_type='text/markdown',
    long_description=long_description,
    url="https://github.com/STTARR/msiimport",
    packages=['msiimport'],
    install_requires=[
        "numpy",
        "nibabel",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)