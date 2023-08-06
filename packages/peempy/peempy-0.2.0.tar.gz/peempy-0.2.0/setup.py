#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

if __name__ == '__main__':
    # Provide static information in setup.json
    # such that it can be discovered automatically

    README_PATH = path.join(path.dirname(__file__), "README.md")
    with open(README_PATH) as f:
        long_desc = f.read()
    setup(packages=find_packages(),
          name="peempy",
          author="Bonan Zhu",
          author_email="bon.zhu@protonmail.com",
          classifiers=[
              "Programming Language :: Python",
              "Development Status :: 5 - Production/Stable"
          ],
          description="Python tool for processing XMCD PEEM data",
          url="https://gitlab.com/bz1/peempy",
          license="MIT License",
          version="0.2.0",
          long_description_content_type='text/markdown',
          long_description=long_desc,
          entry_points={
              "console_scripts": [
                  "peempy_ob=peempy.peembatch:main",
                  "peempy=peempy.cmdline:peemcli",
                  "peemdata=peempy.datawatcher:main"
              ]
          },
          install_requires=[
              "matplotlib", "colorcet", "scikit-image", "tqdm", "scipy",
              "numpy", "click"
          ],
          extras_require={
              'testing': ['pytest'],
              "pre-commit": [
                  "pre-commit",
                  "yapf",
              ]
          })
