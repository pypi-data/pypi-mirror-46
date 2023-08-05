#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Named colors and function definitions. Color names are case-insensitive.
	Extends the CSS references. """

from .._color import Color as _Color
from .._ref import Reference as _Reference
from ._css import CSS4Reference as _CSS4Reference

__all__ = ["DefaultReference"]

class DefaultReference(_CSS4Reference):
	""" Extensions to the CSS Color Module Level 4 reference. """

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	number = _Reference.number
	percentage = _Reference.percentage
	angle = _Reference.angle
	color = _Reference.color

	# ---
	# RGB functions.
	# ---

	def rbg(self, r: number | percentage,
		b: number | percentage = number(0), g: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (0, 2, 1))

	def rbga(self, r: number | percentage,
		b: number | percentage = number(0), g: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (0, 2, 1))

	def brg(self, b: number | percentage,
		r: number | percentage = number(0), g: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (1, 2, 0))

	def brga(self, b: number | percentage,
		r: number | percentage = number(0), g: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (1, 2, 0))

	def bgr(self, b: number | percentage,
		g: number | percentage = number(0), r: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (2, 1, 0))

	def bgra(self, b: number | percentage,
		g: number | percentage = number(0), r: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (2, 1, 0))

	def gbr(self, g: number | percentage,
		b: number | percentage = number(0), r: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (2, 0, 1))

	def gbra(self, g: number | percentage,
		b: number | percentage = number(0), r: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (2, 0, 1))

	def grb(self, g: number | percentage,
		r: number | percentage = number(0), b: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (1, 0, 2))

	def grba(self, g: number | percentage,
		r: number | percentage = number(0), b: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (1, 0, 2))

	# ---
	# HLS and HWB aliases.
	# ---

	def hls(self, h: number | angle, l: number | percentage,
		s: number | percentage, alpha: number | percentage = number(1.0)):
		return self._hsl((h, s, l, alpha), (0, 2, 1))

	def hlsa(self, h: number | angle, l: number | percentage,
		s: number | percentage, alpha: number | percentage = number(1.0)):
		return self._hsl((h, s, l, alpha), (0, 2, 1))

	def hbw(self, h: number | angle, b: number | percentage = number(0),
		w: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._hwb((h, w, b, alpha), (0, 2, 1))

	def hbwa(self, h: number | angle, b: number | percentage = number(0),
		w: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._hwb((h, w, b, alpha), (0, 2, 1))

	# ---
	# Get the RGB components of a color.
	# ---

	def red(self, col: color) -> number:
		r, g, b = col.to_color().rgb()
		return _Reference.number(r)

	def green(self, col: color) -> number:
		r, g, b = col.to_color().rgb()
		return _Reference.number(g)

	def blue(self, col: color) -> number:
		r, g, b = col.to_color().rgb()
		return _Reference.number(b)

	# ---
	# Manage the lightness and saturation for HSL colors.
	# ---

	def darker(self, by: number | percentage, col: color) -> color:
		try:
			by = by.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		try:
			col = col.to_color()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		h, l, s, a = col.hlsa()
		l = max(l - by, 0.0)

		return _Reference.color(_Color(_Color.Type.HSL, h, s, l, a))

	def lighter(self, by: number | percentage, col: color) -> color:
		try:
			by = by.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		try:
			col = col.to_color()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		h, l, s, a = col.hlsa()
		l = min(l + by, 1.0)

		return _Reference.color(_Color(_Color.Type.HSL, h, s, l, a))

	def desaturate(self, by: number | percentage, col: color) -> color:
		try:
			by = by.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		try:
			col = col.to_color()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		h, l, s, a = col.hlsa()
		s = max(s - by, 0.0)

		return _Reference.color(_Color(_Color.Type.HSL, h, s, l, a))

	def saturate(self, by: number | percentage, col: color) -> color:
		try:
			by = by.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		try:
			col = col.to_color()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		h, l, s, a = col.hlsa()
		s = min(s + by, 1.0)

		return _Reference.color(_Color(_Color.Type.HSL, h, s, l, a))

	# ---
	# Others.
	# ---

	def ncol(self, col: color) -> color:
		# Compatibility with w3color.js! NCols are managed directly without
		# the function, so the functio doesn't do anything.

		return col

# End of file.
