import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parallel-bars",
    version="0.0.6",
    author="Maciej Rapacz",
    author_email="python.parallelbars@gmail.com",
    description="Simple wrapper on top of multiprocessing and tqdm progress bars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrapacz/parallel-bars",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
