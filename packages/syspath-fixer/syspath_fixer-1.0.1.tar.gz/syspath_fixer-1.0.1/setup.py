
import os
import sys

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()
from setuptools import setup

setup(
    name="syspath_fixer",
    version="1.0.1",
    url="https://github.com/TeodorIvanov/syspath-fixer",
    license="MIT",
    author="Teodor Ivanov",
    author_email="tdrivanov@gmail.com",
    description="add modules to syspath easily",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["syspath_fixer"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
