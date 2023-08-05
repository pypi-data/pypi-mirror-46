#!/usr/bin/env python3

import setuptools

with open("README.md","r") as fh:
  longdescription = fh.read() 

setuptools.setup(name='cetem_publico',
      version='0.0.4',
      description='Python WRAPPER For CETEM Publico Corpus',
      author='Ezequiel Moreira',
      author_email='pg38413@alunos.uminho.pt',
      packages = setuptools.find_packages(),
      long_description = longdescription
     )
