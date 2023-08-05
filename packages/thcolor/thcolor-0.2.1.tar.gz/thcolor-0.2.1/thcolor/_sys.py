#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Conversions between color systems. """

from math import ceil as _ceil
from colorsys import hls_to_rgb

__all__ = ["hls_to_rgb", "hwb_to_rgb", "netscape_color"]

def hwb_to_rgb(hue, w, b):
	""" Convert HWB to RGB color.
		https://drafts.csswg.org/css-color/#hwb-to-rgb """

	r, g, b = hls_to_rgb(hue, 0.5, 1.0)
	f = lambda x: x * (1 - w - b) + w
	r, g, b = f(r), f(g), f(b)

	return r, g, b

def netscape_color(name):
	""" Produce a color from a name (which can be all-text, all-digits or
		both), using the Netscape behaviour. """

	# Find more about this here: https://stackoverflow.com/a/8333464
	#
	# First of all:
	# - we sanitize our input by replacing invalid characters
	#   by '0' characters (the 0xFFFF limit is due to how
	#   UTF-16 was managed at the time).
	# - we truncate our input to 128 characters.

	name = name.lower()
	name = ''.join(c if c in '0123456789abcdef' \
		else ('0', '00')[ord(c) > 0xFFFF] \
		for c in name[:128])[:128]

	# Then we calculate some values we're going to need.
	# `iv` is the size of the zone for a member.
	# `sz` is the size of the digits slice to take in that zone
	# (max. 8).
	# `of` is the offset in the zone of the slice to take.

	iv = _ceil(len(name) / 3)
	of = iv - 8 if iv > 8 else 0
	sz = iv - of

	# Then we isolate the slices using the values calculated
	# above. `gr` will be an array of 3 or 4 digit strings
	# (depending on the number of members).

	gr = list(map(lambda i: name[i * iv + of:i * iv + iv] \
		.ljust(sz, '0'), range(3)))

	# Check how many digits we can skip at the beginning of
	# each slice.

	pre = min(map(lambda x: len(x) - len(x.lstrip('0')), gr))
	pre = min(pre, sz - 2)

	# Then we extract the values.

	it = map(lambda x: int('0' + x[pre:pre + 2], 16), gr)
	r, g, b = it

	return (r, g, b)

# End of file.
