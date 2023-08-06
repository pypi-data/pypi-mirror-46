from pathlib import Path
import setuptools

# Load version number
version = {}
with open("EasyCo/__version__.py") as fp:
    exec(fp.read(), version)
assert version
assert version['__VERSION__']
__VERSION__ = version['__VERSION__']
print(f'Version: {__VERSION__}')
print('')

# don't load file for tox-builds
readme = Path(__file__).with_name('readme.md')
long_description = ''
if readme.is_file():
    with readme.open("r", encoding='utf-8') as fh:
        long_description = fh.read()

setuptools.setup(
    name="EasyCo",
    version=__VERSION__,
    author="spaceman_spiff",
    # author_email="",
    description="Easy configuration with yaml files",
    keywords=[
        'yaml',
        'yml',
        'config',
        'configuration',
        'file'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spacemanspiff2007/EasyCo",
    project_urls={
        'Documentation': 'https://easyco.readthedocs.io/',
        'GitHub': 'https://github.com/spacemanspiff2007/EasyCo',
    },
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=[
        'ruamel.yaml',
        'voluptuous',
        'watchdog',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ]
)
