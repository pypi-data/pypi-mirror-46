#! /usr/bin/env python

from distutils.core import setup

setup(name="django-jscroll",
      version="1.0.0",
      description="",
      packages=["jscroll", 
      "jscroll.templates", "jscroll.templates.jscroll"],

      package_data={'jscroll.templates.jscroll': ['jscroll.html', 
      'jscroll.html', 'jscroll-window.html'],},

      author="Iury O. G. Figueiredo",
      author_email="ioliveira@id.uff.br",
      url='',
      download_url='',
      keywords=[],
      classifiers=[])



































































