import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magic-carbon",
    #Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/development.html#single-sourcing-the-version
    version="0.0.1",
    author="George Alvarado",
    author_email="georgealvarado@outlook.com",
    description="Un pequeno paquete que hace magia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords = ['carbon', 'datetime', 'django'],
    url="https://gitlab.com/yoryo/magic-carbon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)