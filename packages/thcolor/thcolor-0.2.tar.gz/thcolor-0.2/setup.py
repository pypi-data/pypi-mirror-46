#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor Python 3.x module, which is MIT-licensed.
#******************************************************************************
""" Setup script for the thcolor Python package and script. """

from setuptools import setup as _setup

kwargs = {}

try:
	from sphinx.setup_command import BuildDoc as _BuildDoc
	kwargs['cmdclass'] = {'build_sphinx': _BuildDoc}
except:
	pass

# Actually, most of the project's data is read from the `setup.cfg` file.

_setup(**kwargs)

# End of file.
