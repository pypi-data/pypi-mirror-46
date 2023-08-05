#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" HTML/CSS-like color parsing, mainly for the `[color]` tag.
	Defines the `get_color()` function which returns an rgba value.

	The functions in this module do not aim at being totally compliant with
	the W3C standards, although it is inspired from it.
"""

from ._color import Color
from ._ref import Reference
from ._angle import Angle

from ._exc import ColorExpressionDecodingError
from ._builtin import (CSS1Reference, CSS2Reference, CSS3Reference,
	CSS4Reference, DefaultReference)

__all__ = ["version", "Color", "Reference", "Angle",
	"ColorExpressionDecodingError",
	"CSS1Reference", "CSS2Reference", "CSS3Reference",
	"CSS4Reference", "DefaultReference"]

version = "0.2.2"

# End of file.
