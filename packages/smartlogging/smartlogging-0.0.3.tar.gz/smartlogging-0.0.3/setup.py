import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version_contents = {}
with open(os.path.join('smartlogging', 'version.py')) as f:
    exec(f.read(), version_contents)

setuptools.setup(
    name="smartlogging",
    version="0.0.3",
    author="Maxwell Flitton and Florentin Hortet",
    author_email="maxwellflitton@gmail.com",
    description="Easy smart logging for you python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blue-walkers/smart-logger",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Build Tools"
    ),
    install_requires=[
        "certifi==2019.3.9",
        "chardet==3.0.4",
        "discord-webhook==0.4.1",
        "idna==2.8",
        "peewee==3.9.5",
        "requests==2.22.0",
        "urllib3==1.25.2"
    ],
    zip_safe=False
)
