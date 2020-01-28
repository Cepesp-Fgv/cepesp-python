import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='electionsBR',
    version='0.2',
    author="Abraao Barros",
    author_email="abraaobarros3@gmail.com",
    description="A python wrapper to fetch votes from BR elections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cepesp-Fgv/cepesp-python",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas>=0.25.3',
        'requests>=2.20.1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
