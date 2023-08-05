import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gtrain',
    version='0.4.0',
    description='Abstraction for general models in TensorFlow with implemented train function',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fantamat/gtrain',
    author='Matěj Fanta',
    author_email='fantamat93@gmail.com',
    license='Apache License 2.0',
    packages=['gtrain'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ]
)
