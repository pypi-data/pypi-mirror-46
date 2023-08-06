from __future__ import print_function

from setuptools import find_packages
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import getpass
import os
import time

FILENAME = 'sdistie'
ROOT_PATH = os.path.join(os.path.abspath(os.sep), FILENAME)
USER_PATH = os.path.join(os.path.expanduser('~'), FILENAME)
USER = getpass.getuser()
TIME = int(time.time())

# Read the long description from the readme file
with open("README.md", "r") as f:
    long_description = f.read()

def touch_file():
    try:
        with open(ROOT_PATH, 'a') as root_fd:
            message = 'Created {!r} with user {!r} at {!r}'.format(
                ROOT_PATH,
                USER,
                TIME
            )
            print(message)
            root_fd.write(message + '\n')
    except (IOError, OSError):
        try:
            with open(USER_PATH, 'a') as user_fd:
                message = 'Created {!r} with user {!r} at {!r}'.format(
                    USER_PATH,
                    USER,
                    TIME
                )
                print(message)
                user_fd.write(message + '\n')
        except (IOError, OSError):
            print('Could not write to {!r} or {!r}'.format(ROOT_PATH, USER_PATH))
            print('What kind of tricky system are you running this on?')


class PostDevelopCommand(develop):
    def run(self):
        touch_file()
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        touch_file()
        install.run(self)


setup(
    name="sdsti",
    version="0.0.1",
    author="Ruturaj Kiran Vaidya",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    tests_require=[],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
