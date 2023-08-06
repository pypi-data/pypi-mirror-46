from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'pythoncli',
    version = '1.0.1',
    author="Peter Hassaballah",
    author_email="peter.hassaballah@gmail.com",
    description="A Python CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peterHassaballah/pythoncli",
    install_requires=['fire==0.1.3','pydub==0.23.1','ffmpeg'],
    packages = ['pythoncli'],
    entry_points = {
        'console_scripts': [
            'pythoncli = pythoncli.__main__:main'
        ]
    })