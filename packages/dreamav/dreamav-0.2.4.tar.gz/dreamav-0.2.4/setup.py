import glob
import os
from setuptools import setup, find_packages

from dreamav.__init__ import __ROOT__

def get_requirements():
    ret = []
    with open("./requirements.txt", "r") as f:
        for line in f.readlines():
            ret.append(line.strip())

    return ret


requires = get_requirements()
setup(
    name = 'dreamav',
    version = '0.2.4',
    description = "This package is for detecting malicious document",
    author = ["Damin Moon", "Kihwan Kim", "HyunSeok Kim", "Hyeri Jung", "Yuhan Bang"],
    author_email = "vmfn0401@gmail.com",
    packages=find_packages(),
    data_files = [("model", glob.glob(os.path.join(__ROOT__, "util/model/*"))), ("ini", [os.path.join(__ROOT__, "dream.ini")])],
    setup_requires=requires,
    entry_points = {
        'console_scripts': [
            'dreamav = dreamav.__main__:main'
        ]
    })
