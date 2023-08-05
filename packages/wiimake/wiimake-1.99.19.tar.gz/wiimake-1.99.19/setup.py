import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('wiimake/_version.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='wiimake',
    version=version,
    packages=['wiimake'],
    description='Command line tool for building Gamecube/Wii mods',
    long_description=long_descr,
    author='Tom Sherman',
    author_email='tomsherman159@gmail.com',
    url='https://github.com/sherman5/wiimake',
    entry_points={
        'console_scripts': [
            'wiimake=wiimake.wiimake:main',
            'wiimake-isotool=wiimake.wiimake_isotool:main'
        ]
    }
)
