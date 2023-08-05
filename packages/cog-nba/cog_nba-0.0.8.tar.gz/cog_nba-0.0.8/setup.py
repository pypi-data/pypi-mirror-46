import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cog_nba",
    version="0.0.8",
    author="Andryo Marzuki",
    author_email="stabbish@gmail.com",
    description="A wrapper over the stats.nba.com API which builds in caching of GET queries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://andryo.co",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'sqlalchemy',
        'requests'
    ]
)
