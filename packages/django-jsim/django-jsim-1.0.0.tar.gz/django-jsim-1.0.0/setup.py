#! /usr/bin/env python3

from distutils.core import setup

setup(name="django-jsim",
      version="1.0.0",
      description="",
      packages=["jsim", "jsim.templatetags", 
      "jsim.templates", "jsim.static", "jsim.templates.jsim"],
      package_data={'jsim.templates.jsim': ['jsim.html'], 
      'jsim.static':['jsim.js']},

      author="Iury O. G. Figueiredo",
      author_email="ioliveira@id.uff.br",
      url='',
      download_url='',
      keywords=[],
      classifiers=[])





































































