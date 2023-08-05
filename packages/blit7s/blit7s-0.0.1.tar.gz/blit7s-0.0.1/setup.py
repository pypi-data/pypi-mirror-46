import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blit7s",
    version="0.0.1",
    author="Armaan Aggarwal",
    description="A package for RPi.GPIO that allows you to blit characters on a 7 segment unit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/armaan115/blit7s",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha"
    ],
)
