import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='electionsBR',
    version='0.1',
    author="Abraao Barros",
    author_email="abraaobarros3@gmail.com",
    description="A python wrapper to fetch votes from BR elections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cepesp-Fgv/cepesp-python",
    packages=['electionsBR'],
    install_requires=[
        'pandas',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
