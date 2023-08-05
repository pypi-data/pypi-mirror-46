#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Named colors references, using various sources. """

from ._css import (CSS1Reference, CSS2Reference, CSS3Reference,
	CSS4Reference)
from ._default import DefaultReference

__all__ = ["CSS1Reference", "CSS2Reference", "CSS3Reference",
	"CSS4Reference", "DefaultReference"]

# End of file.
