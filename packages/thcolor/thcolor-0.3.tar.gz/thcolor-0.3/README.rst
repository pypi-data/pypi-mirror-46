thcolor -- the touhey color management module
=============================================

This module is a color management module made by `Thomas Touhey`_ (``th``
is for ``touhey``) for the `textoutpc`_ project, a BBCode to HTML translation
module. It provides the following features:

- color management and conversions between formats (RGB, HSL, HWB, NCol, …).
- text-to-color using close-to-CSS format.

For more information, consult `the official website`_.

Examples
--------

Converting an RGB color to HSL:

.. code-block:: python

	from thcolor import Color

	color = Color(Color.Type.RGB, 55, 23, 224)
	print(color.hsl())

Converting a HSL color to RGB with an alpha value:

.. code-block:: python

	from thcolor import Color, Angle

	alpha = 0.75
	color = Color(Color.Type.HSL, Angle(Angle.Type.DEG, 180), 0.5, 1.0, alpha)
	print(color.rgba())

Converting a textual representation to the RGBA color components:

.. code-block:: python

	from thcolor import Color

	color = Color.from_text("darker(10%,  hsl(0, 1, 50.0%))")
	print(color.rgba())

Getting the CSS color representations (with compatibility for earlier CSS
versions) from a textual representation:

.. code-block:: python

	from thcolor import Color

	color = Color.from_text("gray(red( #123456 )/0.2/)")
	for repres in color.css():
		print(f"color: {repres}")

.. _Thomas Touhey: https://thomas.touhey.fr/
.. _textoutpc: https://textout.touhey.pro/
.. _the official website: https://thcolor.touhey.pro/
