#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Conversions between color systems. """

from math import ceil as _ceil

from ._angle import Angle as _Angle

__all__ = ["hls_to_hwb", "hwb_to_hls", "hls_to_rgb", "rgb_to_hls",
	"rgb_to_hwb", "hwb_to_rgb", "netscape_color"]

# ---
# Color systems conversion utilities.
# ---

def _rgb(r, g, b):
	return tuple(map(lambda x: int(round(x * 255, 0)), (r, g, b)))
def _hls(hue, s, l):
	return _Angle(_Angle.Type.DEG, round(hue, 2)), round(l, 2), round(s, 2)

def hls_to_hwb(hue, l, s):
	""" Convert HWB to HSL. """

	_, w, b = rgb_to_hwb(*hls_to_rgb(hue, l, s))
	return (hue, w, b)

def hwb_to_hls(hue, w, b):
	""" Convert HWB to HLS. """

	_, l, s = rgb_to_hls(*hwb_to_rgb(hue, w, b))
	return (hue, l, s)

def hls_to_rgb(hue, l, s):
	""" Convert HLS to RGB. """

	if s == 0:
		# Achromatic color.

		return l, l, l

	def _hue_to_rgb(t1, t2, hue):
		hue %= 6

		if   hue < 1:
			return t1 + (t2 - t1) * hue
		elif hue < 3:
			return t2
		elif hue < 4:
			return t1 + (t2 - t1) * (4 - hue)
		return t1

	hue = (hue.degrees % 360) / 60
	if l <= 0.5:
		t2 = l * (s + 1)
	else:
		t2 = l + s - (l * s)

	t1 = l * 2 - t2

	return _rgb(\
		_hue_to_rgb(t1, t2, hue + 2),
		_hue_to_rgb(t1, t2, hue),
		_hue_to_rgb(t1, t2, hue - 2))

def hwb_to_rgb(hue, w, bl):
	""" Convert HWB to RGB color.
		https://drafts.csswg.org/css-color/#hwb-to-rgb """

	r, g, b = map(lambda x: x / 255, hls_to_rgb(hue, 0.5, 1.0))
	if w + bl > 1:
		w, bl = map(lambda x: x / (w + bl), (w, bl))
	return _rgb(*map(lambda x: x * (1 - w - bl) + w, (r, g, b)))

def rgb_to_hls(r, g, b):
	""" Convert RGB to HLS. """

	r, g, b = map(lambda x: x / 255, (r, g, b))

	min_value = min((r, g, b))
	max_value = max((r, g, b))
	chroma = max_value - min_value

	if   chroma == 0:
		hue = 0
	elif r == max_value:
		hue = (g - b) / chroma
	elif g == max_value:
		hue = (b - r) / chroma + 2
	else:
		hue = (r - g) / chroma + 4

	hue = hue * 60 + (hue < 0) * 360
	l = (min_value + max_value) / 2
	if min_value == max_value:
		s = 0
	else:
		s = max_value - min_value
		if l < 0.5:
			s /= max_value + min_value
		else:
			s /= 2 - max_value - min_value

	return _hls(hue, l, s)

def rgb_to_hwb(r, g, b):
	""" Convert RGB to HWB. """

	r, g, b = map(lambda x: x / 255, (r, g, b))

	max_value = max((r, g, b))
	min_value = min((r, g, b))
	chroma = max_value - min_value

	if   chroma == 0:
		hue = 0
	elif r == max_value:
		hue = (g - b) / chroma
	elif g == max_value:
		hue = (b - r) / chroma + 2
	elif g == max_value:
		hue = (r - g) / chroma + 4

	hue = (hue % 6) * 360
	w = min_value
	b = max_value

	return _Angle(_Angle.Type.DEG, hue), w, b

# ---
# Other utilities.
# ---

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
