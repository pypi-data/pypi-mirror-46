import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="climatempo",
    version="0.0.1",
    author="Julio Manuel Blanco Perez",
    author_email="jblancoperez@gmail.com",
    description="Simple wrapper for climatempo API (just to abstract home assistant)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jblancoperez/climatempo",
    install_requires = ['requests==2.21.0'],
    packages=['climatempo'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

