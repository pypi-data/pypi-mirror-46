import os

from setuptools import setup


def readme_file_contents():
    readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'README.rst')
    with open(readme_path) as readme_file:
        file_contents = readme_file.read()
    return file_contents


setup(
    name='blirupgameoflife',
    version='1.0.5',
    description='Conway\'s Game of Life implemented with PyGame',
    long_description=readme_file_contents(),
    url='https://github.com/Blirup/gameoflife.git',
    author='Blirup',
    author_email='martin.blirup@gmail.com',
    license='GPL-3.0',
    packages=['blirupgameoflife'],
    scripts=[
        'bin/blirupgameoflife',
        'bin/blirupgameoflife.bat',
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)