#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Named colors and function definitions. Color names are case-insensitive.
	Taken from: https://www.w3schools.com/cssref/css_colors.asp """

from .._color import Color as _Color
from .._ref import Reference as _Reference
from .._exc import InvalidArgumentValueError as _InvalidArgumentValueError

__all__ = ["CSS1Reference", "CSS2Reference", "CSS3Reference",
	"CSS4Reference"]

def _rgb(hex):
	return _Color.from_text(hex, _Reference())

class CSS1Reference(_Reference):
	""" Named colors from CSS Level 1:
		https://www.w3.org/TR/CSS1/ """

	number = _Reference.number
	percentage = _Reference.percentage
	color = _Reference.color

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# ---
	# Named colors.
	# ---

	__colors = {
		'black':   _rgb('#000000'),
		'silver':  _rgb('#c0c0c0'),
		'gray':    _rgb('#808080'),
		'white':   _rgb('#ffffff'),

		'maroon':  _rgb('#800000'),
		'red':     _rgb('#ff0000'),
		'purple':  _rgb('#800080'),
		'fuchsia': _rgb('#ff00ff'),
		'green':   _rgb('#008000'),
		'lime':    _rgb('#00ff00'),
		'olive':   _rgb('#808000'),
		'yellow':  _rgb('#ffff00'),
		'navy':    _rgb('#000080'),
		'blue':    _rgb('#0000ff'),
		'teal':    _rgb('#008080'),
		'aqua':    _rgb('#00ffff')}

	def _color(self, name):
		if name == 'transparent':
			return _Color(_Color.Type.RGB, 0, 0, 0, 0)

		try:
			return self.__colors[name]
		except:
			return super()._color(name)

	# ---
	# Utilities.
	# ---

	def _rgb(self, rgba, rgb_indexes):
		r, g, b, alpha = rgba
		ri, gi, bi = rgb_indexes

		try:
			r = r.to_byte()
		except ValueError as e:
			raise _InvalidArgumentValueError(ri, str(e))

		try:
			g = g.to_byte()
		except ValueError as e:
			raise _InvalidArgumentValueError(gi, str(e))

		try:
			b = b.to_byte()
		except ValueError as e:
			raise _InvalidArgumentValueError(bi, str(e))

		try:
			alpha = alpha.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(3, str(e))

		return _Reference.color(_Color(_Color.Type.RGB, r, g, b, alpha))

	# ---
	# Functions.
	# ---

	def rgb(self, r: number | percentage,
		g: number | percentage = number(0),
		b: number | percentage = number(0)):
		return self._rgb((r, g, b, 1.0), (0, 1, 2))

class CSS2Reference(CSS1Reference):
	""" Named colors from CSS Level 2 (Revision 1):
		https://www.w3.org/TR/CSS2/ """

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# ---
	# Named colors.
	# ---

	__colors = {
		'orange': _rgb('#ffa500')}

	def _color(self, name):
		try:
			return self.__colors[name]
		except:
			return super()._color(name)

class CSS3Reference(CSS2Reference):
	""" Named colors from CSS Color Module Level 3:
		https://drafts.csswg.org/css-color-3/ """

	number = _Reference.number
	percentage = _Reference.percentage
	angle = _Reference.angle
	color = _Reference.color

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	# ---
	# Named colors.
	# ---

	__colors = {
		'darkblue':             _rgb('#00008B'),
		'mediumblue':           _rgb('#0000CD'),
		'darkgreen':            _rgb('#006400'),
		'darkcyan':             _rgb('#008B8B'),
		'deepskyblue':          _rgb('#00BFFF'),
		'darkturquoise':        _rgb('#00CED1'),
		'mediumspringgreen':    _rgb('#00FA9A'),
		'springgreen':          _rgb('#00FF7F'),
		'cyan':                 _rgb('#00FFFF'),
		'midnightblue':         _rgb('#191970'),
		'dodgerblue':           _rgb('#1E90FF'),
		'lightseagreen':        _rgb('#20B2AA'),
		'forestgreen':          _rgb('#228B22'),
		'seagreen':             _rgb('#2E8B57'),
		'darkslategray':        _rgb('#2F4F4F'),
		'darkslategrey':        _rgb('#2F4F4F'),
		'limegreen':            _rgb('#32CD32'),
		'mediumseagreen':       _rgb('#3CB371'),
		'turquoise':            _rgb('#40E0D0'),
		'royalblue':            _rgb('#4169E1'),
		'steelblue':            _rgb('#4682B4'),
		'darkslateblue':        _rgb('#483D8B'),
		'mediumturquoise':      _rgb('#48D1CC'),
		'indigo':               _rgb('#4B0082'),
		'darkolivegreen':       _rgb('#556B2F'),
		'cadetblue':            _rgb('#5F9EA0'),
		'cornflowerblue':       _rgb('#6495ED'),
		'mediumaquamarine':     _rgb('#66CDAA'),
		'dimgray':              _rgb('#696969'),
		'dimgrey':              _rgb('#696969'),
		'slateblue':            _rgb('#6A5ACD'),
		'olivedrab':            _rgb('#6B8E23'),
		'slategray':            _rgb('#708090'),
		'slategrey':            _rgb('#708090'),
		'lightslategray':       _rgb('#778899'),
		'lightslategrey':       _rgb('#778899'),
		'mediumslateblue':      _rgb('#7B68EE'),
		'lawngreen':            _rgb('#7CFC00'),
		'chartreuse':           _rgb('#7FFF00'),
		'aquamarine':           _rgb('#7FFFD4'),
		'grey':                 _rgb('#808080'),
		'skyblue':              _rgb('#87CEEB'),
		'lightskyblue':         _rgb('#87CEFA'),
		'blueviolet':           _rgb('#8A2BE2'),
		'darkred':              _rgb('#8B0000'),
		'darkmagenta':          _rgb('#8B008B'),
		'saddlebrown':          _rgb('#8B4513'),
		'darkseagreen':         _rgb('#8FBC8F'),
		'lightgreen':           _rgb('#90EE90'),
		'mediumpurple':         _rgb('#9370DB'),
		'darkviolet':           _rgb('#9400D3'),
		'palegreen':            _rgb('#98FB98'),
		'darkorchid':           _rgb('#9932CC'),
		'yellowgreen':          _rgb('#9ACD32'),
		'sienna':               _rgb('#A0522D'),
		'brown':                _rgb('#A52A2A'),
		'darkgray':             _rgb('#A9A9A9'),
		'darkgrey':             _rgb('#A9A9A9'),
		'lightblue':            _rgb('#ADD8E6'),
		'greenyellow':          _rgb('#ADFF2F'),
		'paleturquoise':        _rgb('#AFEEEE'),
		'lightsteelblue':       _rgb('#B0C4DE'),
		'powderblue':           _rgb('#B0E0E6'),
		'firebrick':            _rgb('#B22222'),
		'darkgoldenrod':        _rgb('#B8860B'),
		'mediumorchid':         _rgb('#BA55D3'),
		'rosybrown':            _rgb('#BC8F8F'),
		'darkkhaki':            _rgb('#BDB76B'),
		'mediumvioletred':      _rgb('#C71585'),
		'indianred':            _rgb('#CD5C5C'),
		'peru':                 _rgb('#CD853F'),
		'chocolate':            _rgb('#D2691E'),
		'tan':                  _rgb('#D2B48C'),
		'lightgray':            _rgb('#D3D3D3'),
		'lightgrey':            _rgb('#D3D3D3'),
		'thistle':              _rgb('#D8BFD8'),
		'orchid':               _rgb('#DA70D6'),
		'goldenrod':            _rgb('#DAA520'),
		'palevioletred':        _rgb('#DB7093'),
		'crimson':              _rgb('#DC143C'),
		'gainsboro':            _rgb('#DCDCDC'),
		'plum':                 _rgb('#DDA0DD'),
		'burlywood':            _rgb('#DEB887'),
		'lightcyan':            _rgb('#E0FFFF'),
		'lavender':             _rgb('#E6E6FA'),
		'darksalmon':           _rgb('#E9967A'),
		'violet':               _rgb('#EE82EE'),
		'palegoldenrod':        _rgb('#EEE8AA'),
		'lightcoral':           _rgb('#F08080'),
		'khaki':                _rgb('#F0E68C'),
		'aliceblue':            _rgb('#F0F8FF'),
		'honeydew':             _rgb('#F0FFF0'),
		'azure':                _rgb('#F0FFFF'),
		'sandybrown':           _rgb('#F4A460'),
		'wheat':                _rgb('#F5DEB3'),
		'beige':                _rgb('#F5F5DC'),
		'whitesmoke':           _rgb('#F5F5F5'),
		'mintcream':            _rgb('#F5FFFA'),
		'ghostwhite':           _rgb('#F8F8FF'),
		'salmon':               _rgb('#FA8072'),
		'antiquewhite':         _rgb('#FAEBD7'),
		'linen':                _rgb('#FAF0E6'),
		'lightgoldenrodyellow': _rgb('#FAFAD2'),
		'oldlace':              _rgb('#FDF5E6'),
		'magenta':              _rgb('#FF00FF'),
		'deeppink':             _rgb('#FF1493'),
		'orangered':            _rgb('#FF4500'),
		'tomato':               _rgb('#FF6347'),
		'hotpink':              _rgb('#FF69B4'),
		'coral':                _rgb('#FF7F50'),
		'darkorange':           _rgb('#FF8C00'),
		'lightsalmon':          _rgb('#FFA07A'),
		'lightpink':            _rgb('#FFB6C1'),
		'pink':                 _rgb('#FFC0CB'),
		'gold':                 _rgb('#FFD700'),
		'peachpuff':            _rgb('#FFDAB9'),
		'navajowhite':          _rgb('#FFDEAD'),
		'moccasin':             _rgb('#FFE4B5'),
		'bisque':               _rgb('#FFE4C4'),
		'mistyrose':            _rgb('#FFE4E1'),
		'blanchedalmond':       _rgb('#FFEBCD'),
		'papayawhip':           _rgb('#FFEFD5'),
		'lavenderblush':        _rgb('#FFF0F5'),
		'seashell':             _rgb('#FFF5EE'),
		'cornsilk':             _rgb('#FFF8DC'),
		'lemonchiffon':         _rgb('#FFFACD'),
		'floralwhite':          _rgb('#FFFAF0'),
		'snow':                 _rgb('#FFFAFA'),
		'lightyellow':          _rgb('#FFFFE0'),
		'ivory':                _rgb('#FFFFF0')}

	def _color(self, name):
		try:
			return self.__colors[name]
		except:
			return super()._color(name)

	# ---
	# Utilities.
	# ---

	def _hsl(self, hsla, hsl_indexes):
		h, s, l, alpha = hsla
		hi, si, li = hsl_indexes

		try:
			h = h.to_hue()
		except ValueError as e:
			raise _InvalidArgumentValueError(hi, str(e))

		try:
			s = s.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(si, str(e))

		try:
			l = l.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(li, str(e))

		try:
			alpha = alpha.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(3, str(e))

		return _Reference.color(_Color(_Color.Type.HSL, h, s, l, alpha))

	# ---
	# Functions.
	# ---

	def rgb(self, r: number | percentage,
		g: number | percentage = number(0), b: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (0, 1, 2))

	def rgba(self, r: number | percentage,
		g: number | percentage = number(0), b: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._rgb((r, g, b, alpha), (0, 1, 2))

	def hsl(self, h: number | angle, s: number | percentage,
		l: number | percentage, alpha: number | percentage = number(1.0)):
		return self._hsl((h, s, l, alpha), (0, 1, 2))

	def hsla(self, h: number | angle, s: number | percentage,
		l: number | percentage, alpha: number | percentage = number(1.0)):
		return self._hsl((h, s, l, alpha), (0, 1, 2))

class CSS4Reference(CSS3Reference):
	""" Named colors from CSS Color Module Level 4:
		https://drafts.csswg.org/css-color/ """

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	number = _Reference.number
	percentage = _Reference.percentage
	angle = _Reference.angle
	color = _Reference.color

	# ---
	# Named colors.
	# ---

	__colors = {
		'rebeccapurple': _rgb('#663399')}

	def _color(self, name):
		try:
			return self.__colors[name]
		except:
			return super()._color(name)

	# ---
	# Utilities.
	# ---

	def _hwb(self, hwba, hwb_indexes):
		h, w, b, alpha = hwba
		hi, wi, bi = hwb_indexes

		try:
			h = h.to_hue()
		except ValueError as e:
			raise _InvalidArgumentValueError(hi, str(e))

		try:
			w = w.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(wi, str(e))

		try:
			b = b.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(bi, str(e))

		try:
			alpha = alpha.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(3, str(e))

		return _Reference.color(_Color(_Color.Type.HWB, h, w, b, alpha))

	# ---
	# Functions.
	# ---

	def hwb(self, h: number | angle, w: number | percentage = number(0),
		b: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._hwb((h, w, b, alpha), (0, 1, 2))

	def hwba(self, h: number | angle, w: number | percentage = number(0),
		b: number | percentage = number(0),
		alpha: number | percentage = number(1.0)):
		return self._hwb((h, w, b, alpha), (0, 1, 2))

	def gray(self, g: number | percentage, alpha: percentage = number(1.0)):
		try:
			g = g.to_byte()
		except ValueError as e:
			raise _InvalidArgumentValueError(0, str(e))

		try:
			alpha = alpha.to_factor()
		except ValueError as e:
			raise _InvalidArgumentValueError(1, str(e))

		return _Reference.color(_Color(_Color.Type.RGB, g, g, g, alpha))

	def lab(self, l: number, a: number, b: number,
		alpha: percentage = number(1.0)):
		raise NotImplementedError

	def lch(self, l: number, c: number, h: number | angle,
		alpha: percentage = number(1.0)):
		raise NotImplementedError

# End of file.
