import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BWStatsWrapper",
    version="0.0.6",
    author="Heknon",
    author_email="heknonplayz@gmail.com",
    description="Easily access Bedwars stats of a Hypixel player.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = [            
    	'requests',
        'pathlib',
      ],
    url="https://github.com/Heknon/BedwarsStatsWrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)