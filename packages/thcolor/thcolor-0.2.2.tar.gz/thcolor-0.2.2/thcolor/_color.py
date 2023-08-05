#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" HTML/CSS like color parsing, mainly for the `[color]` tag.
	Defines the `get_color()` function which returns an rgba value. """

from enum import Enum as _Enum
from warnings import warn as _warn

try:
	import regex as _re
except ImportError:
	_warn("could not import regex, trying the default `re` module.",
		RuntimeWarning)
	import re as _re

from ._ref import Reference as _Reference
from ._angle import Angle as _Angle
from ._sys import (hls_to_rgb as _hls_to_rgb, hwb_to_rgb as _hwb_to_rgb,
	netscape_color as _netscape_color)
from ._exc import (\
	ColorExpressionDecodingError as _ColorExpressionDecodingError,
	NotEnoughArgumentsError as _NotEnoughArgumentsError,
	TooManyArgumentsError as _TooManyArgumentsError,
	InvalidArgumentTypeError as _InvalidArgumentTypeError,
	InvalidArgumentValueError as _InvalidArgumentValueError)

__all__ = ["Color"]

# ---
# Decoding utilities.
# ---

_ColorPattern = _re.compile(r"""
	(
	    ((?P<agl_val>-? ([0-9]+\.?|[0-9]*\.[0-9]+)) \s*
		 (?P<agl_typ>deg|grad|rad|turn))
	  | ((?P<per>[0-9]+(\.[0-9]*)? | \.[0-9]+) \s* \%)
	  |  (?P<num>[0-9]+(\.[0-9]*)? | \.[0-9]+)
	  |  (\# (?P<hex>[0-9a-f]{3} | [0-9a-f]{4} | [0-9a-f]{6} | [0-9a-f]{8}))
	  |  ((?P<name>[a-z]([a-z0-9\s_-]*[a-z0-9_-])?)
		  ( \s* \( \s* (?P<arg> (?0)? ) \s* \) )?)
	)

	\s* ((?P<sep>[,/\s]) \s* (?P<nextargs> (?0))?)?
""", _re.VERBOSE | _re.I | _re.M)

# ---
# Color initialization varargs utilities.
# ---

def _byte(name, value):
	try:
		assert value == int(value)
		assert 0 <= value < 256
	except (AssertionError, TypeError, ValueError):
		raise ValueError(f"{name} should be a byte between 0 and 255") \
			from None

	return value

def _percentage(name, value):
	try:
		assert value == float(value)
		assert 0.0 <= value <= 1.0
	except (AssertionError, TypeError, ValueError):
		raise ValueError(f"{name} should be a proportion between 0 " \
			"and 1.0") from None

	return value

def _hue(name, value):
	if isinstance(value, _Angle):
		pass
	else:
		try:
			value = _Angle(value)
		except:
			raise ValueError(f"{name} should be an Angle instance")

	return value

# ---
# Color class definition.
# ---

class _ColorType(_Enum):
	""" The color type. """

	""" Invalid color. """
	INVALID = 0

	""" RGB/A color. """
	RGB     = 1

	""" HSL/A color. """
	HSL     = 2

	""" HWB/A color. """
	HWB     = 3

class Color:
	""" Represent a color with all of its available formats. """

	# Properties to work with:
	#
	# `_type`: the type as one of the `Color.Type` constants.
	# `_alpha`: alpha value.
	# `_r`, `_g`, `_b`: rgb components, as bytes.
	# `_hue`: hue for HSL and HWB notations.
	# `_sat`, `_lgt`: saturation and light for HSL.
	# `_wht`, `_blk`: whiteness and blackness for HWB.

	Type = _ColorType

	def __init__(self, *args, **kwargs):
		self._type = Color.Type.INVALID
		self.set(*args, **kwargs)

	def __repr__(self):
		args = (('type', self._type),)
		if   self._type == Color.Type.RGB:
			args += (('red', self._r), ('green', self._g), ('blue', self._b))
		elif self._type == Color.Type.HSL:
			args += (('hue', self._hue), ('saturation', self._sat),
				('lightness', self._lgt))
		elif self._type == Color.Type.HWB:
			args += (('hue', self._hue), ('whiteness', self._wht),
				('blackness', self._blk))

		args += (('alpha', self._alpha),)

		argtext = ', '.join(f'{key}: {repr(value)}' for key, value in args)
		return f"{self.__class__.__name__}({argtext})"

	# ---
	# Management methods.
	# ---

	def set(self, *args, **kwargs):
		""" Set the color. """

		args = list(args)

		def _decode_varargs(*keys):
			# Check for each key.

			results = ()

			for names, convert_func, *value in keys:
				for name in names:
					if name in kwargs:
						if args:
							raise TypeError(f"{self.__class__.__name__}() " \
								f"got multiple values for argument {name}")

						raw_result = kwargs.pop(name)
						break
				else:
					name = names[0]
					if args:
						raw_result = args.pop(0)
					elif value:
						raw_result = value[0] if len(value) == 1 else value
					else:
						raise TypeError(f"{self.__class__.__name__}() " \
							"missing a required positional argument: " \
							f"{name}")

				result = convert_func(name, raw_result)
				results += (result,)

			# Check for keyword arguments for which keys are not in the set.

			if kwargs:
				raise TypeError(f"{next(iter(kwargs.keys()))} is an invalid " \
					f"keyword argument for type {type}")

			return results

		# ---
		# Main function body.
		# ---

		# Check for the type.

		if args:
			try:
				type = kwargs.pop('type')
			except:
				type = args.pop(0)
			else:
				if isinstance(args[0], Color.Type):
					raise TypeError(f"{self.__class__.__name__}() got " \
						"multiple values for argument 'type'")
		else:
			try:
				type = kwargs.pop('type')
			except:
				type = self._type
				if type == Color.Type.INVALID:
					raise TypeError(f"{self.__class__.__name__}() missing " \
						"required argument: 'type'")

		try:
			type = Color.Type(type)
		except:
			type = Color.Type.RGB

		# Initialize the properties.

		if   type == Color.Type.RGB:
			self._r, self._g, self._b, self._alpha = _decode_varargs(\
				(('r', 'red'),   _byte),
				(('g', 'green'), _byte),
				(('b', 'blue'),  _byte),
				(('a', 'alpha'), _percentage, 1.0))
		elif type == Color.Type.HSL:
			self._hue, self._sat, self._lgt, self._alpha = _decode_varargs(\
				(('h', 'hue'),                       _hue),
				(('s', 'sat', 'saturation'),         _percentage),
				(('l', 'lig', 'light', 'lightness'), _percentage),
				(('a', 'alpha'),                     _percentage, 1.0))
		elif type == Color.Type.HWB:
			self._hue, self._wht, self._blk, self._alpha = _decode_varargs(\
				(('h', 'hue'),                _hue),
				(('w', 'white', 'whiteness'), _percentage),
				(('b', 'black', 'blackness'), _percentage),
				(('a', 'alpha'),              _percentage, 1.0))
		else:
			raise ValueError(f"invalid color type: {type}")

		# Once the arguments have been tested to be valid, we can set the
		# type.

		self._type = type

	# ---
	# Properties.
	# ---

	@property
	def type(self):
		""" Get the type. """

		return self._type

	@property
	def alpha(self):
		""" Get the alpha. """

		return self._alpha

	@property
	def a(self):
		""" Alias for the `alpha` property. """

		return self.alpha

	@property
	def red(self):
		""" Get the red component. """

		r, _, _ = self.rgb()
		return r

	@property
	def r(self):
		""" Alias for the `red` property. """

		return self.r

	@property
	def green(self):
		""" Get the green component. """

		_, g, _ = self.rgb()
		return g

	@property
	def g(self):
		""" Alias for the `green` property. """

		return self.green

	@property
	def blue(self):
		""" Get the blue component. """

		_, _, b = self.rgb()
		return b

	@property
	def b(self):
		""" Alias for the `blue` property. """

		return self.blue

	# ---
	# Conversion methods.
	# ---

	def rgb(self):
		""" Get the (red, green, blue) components of the color. """

		if   self._type == Color.Type.RGB:
			return (self._r, self._g, self._b)
		elif self._type == Color.Type.HSL:
			r, g, b = map(lambda x: int(x * 255),
				_hls_to_rgb(self._hue.turns % 1, self._lgt, self._sat))
			return (r, g, b)
		elif self._type == Color.Type.HWB:
			r, g, b = map(lambda x: int(x * 255),
				_hwb_to_rgb(self._hue.turns % 1, self._wht, self._blk))
			return (r, g, b)

		raise ValueError(f"color type {self._type} doesn't translate to rgb")

	def rgba(self):
		""" Get the (red, green, blue, alpha) components of the color. """

		r, g, b = self.rgb()
		alpha = self._alpha

		return (r, g, b, alpha)

	def css(self):
		""" Get the CSS declarations (with compatibility management). """

		def statements():
			# Start by yelling a #RRGGBB color, compatible with most
			# web browsers around the world, followed by the rgba()
			# notation if the alpha value isn't 1.0.

			r, g, b, a = self.rgba()
			a = round(a, 3)
			yield f'#{r:02X}{g:02X}{b:02X}'

			if a < 1.0:
				yield f'rgba({r}, {g}, {b}, {round(a, 3) * 100}%)'

			# Then yield more specific CSS declarations in case
			# they're supported (which would be neat!).

			if   self._type == Type.HSL:
				s = round(self._sat, 5) * 100
				l = round(self._lgt, 5) * 100

				if a < 1.0:
					yield f'hsla({self._hue}, {s}%, {l}%, {a})'
				else:
					yield f'hsl({self._hue}, {s}%, {l}%)'
			elif self._type == Type.HWB:
				w = round(self._wht, 5) * 100
				b = round(self._blk, 5) * 100

				if a < 1.0:
					yield f'hwba({self._hue}, {w}%, {b}%, {a})'
				else:
					yield f'hwb({self._hue}, {w}%, {b}%)'

		return list(statements())

	# ---
	# Static methods for decoding.
	# ---

	def from_str(*args, **kwargs):
		""" Alias for `from_text()`. """

		return Color.from_text(value)

	def from_string(*args, **kwargs):
		""" Alias for `from_text()`. """

		return Color.from_text(value)

	def from_text(expr, ref = None):
		""" Get a color from a string. """

		if ref is None:
			ref = _Reference.default()
		if not isinstance(ref, _Reference):
			raise ValueError("ref is expected to be a subclass of Reference")

		class argument:
			def __init__(self, column, value):
				self._column = column
				self._value = value

			def __repr__(self):
				return f"{self.__class__.__name__}(column = {self._column}, " \
					f"value = {repr(self._value)})"

			@property
			def column(self):
				return self._column

			@property
			def value(self):
				return self._value

		def recurse(column, match):
			if not match:
				return ()

			if   match['agl_val'] is not None:
				# The matched value is an angle.

				agl_typ = {
					'deg':  _Angle.Type.DEG,
					'grad': _Angle.Type.GRAD,
					'rad':  _Angle.Type.RAD,
					'turn': _Angle.Type.TURN}[match['agl_typ']]

				value = _Reference.angle(_Angle(agl_typ,
					float(match['agl_val'])))
			elif match['per'] is not None:
				# The matched value is a percentage.

				value = float(match['per'])
				value = _Reference.percentage(value)
			elif match['num'] is not None:
				# The matched value is a number.

				value = _Reference.number(match['num'])
			elif match['hex'] is not None:
				# The matched value is a hex color.

				name = match['hex']

				if len(name) <= 4:
					name = ''.join(map(lambda x: x + x, name))

				r = int(name[0:2], 16)
				g = int(name[2:4], 16)
				b = int(name[4:6], 16)
				a = int(name[6:8], 16) / 255.0 if len(name) == 8 else 1.0

				value = _Reference.color(Color(Color.Type.RGB, r, g, b, a))
			elif match['arg'] is not None:
				# The matched value is a function.

				name = match['name']

				# Get the arguments.

				args = recurse(column + match.start('arg'),
					_ColorPattern.fullmatch(match['arg']))

				# Get the function and call it with the arguments.

				try:
					func = ref.functions[name]
				except KeyError:
					raise _ColorExpressionDecodingError("no such function " \
						f"{repr(name)}", column = column)

				try:
					value = func(*map(lambda x: x.value, args))
				except _NotEnoughArgumentsError as e:
					raise _ColorExpressionDecodingError("not enough " \
						f"arguments (expected at least {e.count} arguments)",
						column = column, func = name)
				except _TooManyArgumentsError as e:
					raise _ColorExpressionDecodingError("extraneous " \
						f"argument (expected {e.count} arguments at most)",
						column = args[e.count].column, func = name)
				except _InvalidArgumentTypeError as e:
					raise _ColorExpressionDecodingError("type mismatch for " \
						f"argument {e.index + 1}: expected {e.expected}, " \
						f"got {e.got}", column = args[e.index].column,
						func = name)
				except _InvalidArgumentValueError as e:
					raise _ColorExpressionDecodingError("erroneous value " \
						f"for argument {e.index + 1}: {e.text}",
						column = args[e.index].column, func = name)
				except NotImplementedError:
					raise _ColorExpressionDecodingError("not implemented",
						column = column, func = name)
			else:
				# The matched value is a named color.

				name = match['name']

				try:
					# Get the named color (e.g. 'blue').

					value = ref.colors[name]
					assert value != None
				except:
					r, g, b = _netscape_color(name)
					value = Color(Color.Type.RGB, r, g, b, 1.0)

				value = _Reference.color(value)

			return (argument(column, value),) \
				+ recurse(column + match.start('nextargs'),
				_ColorPattern.fullmatch(match['nextargs'] or ""))

		# Strip the expression.

		lexpr = expr.strip()
		column = (len(expr) - len(lexpr))
		expr = lexpr
		del lexpr

		# Match the expression (and check it as a whole directly).

		match = _ColorPattern.fullmatch(expr)
		if match is None:
			raise _ColorExpressionDecodingError("expression parsing failed")

		# Get the result and check its type.

		results = recurse(column, match)
		if len(results) > 1:
			raise _ColorExpressionDecodingError("extraneous value",
				column = results[1].column)

		result = results[0].value
		try:
			result = result.to_color()
		except AttributeError:
			raise _ColorExpressionDecodingError("expected a color",
				column = column)

		return result

# End of file.
