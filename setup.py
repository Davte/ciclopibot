"""Setup."""

import codecs
import os
import re
import setuptools
import sys

if sys.version_info < (3, 5):
    raise RuntimeError("Python3.5+ is needed to run async code")

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Read file in `part.part.part.part.ext`.

    Start from `here` and follow the path given by `*parts`
    """
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_information(info, *file_path_parts):
    """Read information in file."""
    version_file = read(*file_path_parts)
    version_match = re.search(
        r"^__{info}__ = ['\"]([^'\"]*)['\"]".format(
            info=info
        ),
        version_file,
        re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='ciclopibot',
    version=find_information("version", "ciclopibot", "__init__.py"),
    author=find_information("author", "ciclopibot", "__init__.py"),
    author_email=find_information("email", "ciclopibot", "__init__.py"),
    description=(
        "Telegram bot based on `davtelepot` providing information about "
        "CicloPi, the public bike-sharing service in Pisa."
    ),
    license=find_information("license", "ciclopibot", "__init__.py"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gogs.davte.it/davte/ciclopibot",
    packages=setuptools.find_packages(),
    platforms=['any'],
    install_requires=[
        'davtelepot',
    ],
    python_requires='>=3.5',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: Chat",
    ],
    keywords='telegram bot python asyncio async aiohttp davtelepot '
             'ciclopi bikesharing bicincitta bicincittà pisa bike',
    include_package_data=True,
)
