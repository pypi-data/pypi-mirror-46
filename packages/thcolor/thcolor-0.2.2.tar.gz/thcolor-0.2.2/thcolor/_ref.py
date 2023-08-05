#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Named color reference, parent class. """

from inspect import (getfullargspec as _getfullargspec,
	getmembers as _getmembers, ismethod as _ismethod)
from itertools import count as _count

from ._angle import Angle as _Angle
from ._sys import netscape_color as _netscape_color
from ._exc import (NotEnoughArgumentsError as _NotEnoughArgumentsError,
	TooManyArgumentsError as _TooManyArgumentsError,
	InvalidArgumentTypeError as _InvalidArgumentTypeError)

__all__ = ["Reference"]

_default_reference = None
_color_cls = None

def _get_color_class():
	global _color_cls

	if _color_cls is not None:
		return _color_cls

	from ._color import Color
	_color_cls = Color
	return _color_cls

class _type_or:
	""" A type or another. """

	def __init__(self, type1, type2):
		self._type1 = type1
		self._type2 = type2

	@property
	def type1(self):
		return self._type1

	@property
	def type2(self):
		return self._type2

	def __repr__(self):
		return f"{repr(self._type1)} | {repr(self._type2)}"

	def __str__(self):
		return f"{self._type1} or {self._type2}"

	def __or__(self, other):
		return type_or(self, other)

	def __contains__(self, other):
		return other in self._type1 or other in self._type2

# ---
# Main reference definition.
# ---

class Reference:
	""" Function reference for color parsing and operations. """

	def __init__(self):
		pass

	# ---
	# Base type and function definitions for parsing.
	# ---

	class base_type(type):
		""" The metaclass for all types used below. """

		def __new__(mcls, name, bases, attrs):
			return super().__new__(mcls, name, bases, attrs)

		def __init__(self, name, bases, attrs):
			self.__name = name

		def __contains__(self, other):
			return self if other == self else None

		def __or__(self, other):
			return _type_or(self, other)

		def __repr__(self):
			return f"<class {repr(self.__name)}>"

		def __str__(self):
			return self.__name

	class number(metaclass = base_type):
		""" The number type. """

		def __init__(self, value):
			if   type(value) == str:
				self._strvalue = value
				self._value = float(value)
			else:
				self._value = float(value)
				if self._value == int(self._value):
					self._strvalue = str(int(self._value))
				else:
					self._strvalue = str(value)

		def to_byte(self):
			try:
				value = int(self._value)

				assert value == self._value
				assert 0 <= value < 256
			except:
				raise ValueError("unsuitable value for byte conversion: " \
					f"{repr(self._value)}")

			return value

		def to_factor(self):
			try:
				assert 0.0 <= self._value <= 1.0
			except:
				raise ValueError("expected a value between 0.0 and 1.0, got " \
					f"{self._value}")

			return self._value

		def to_color(self):
			r, g, b = _netscape_color(self._strvalue)
			Color = _get_color_class()
			return Color(Color.Type.RGB, r, g, b, 1.0)

		def to_hue(self):
			return _Angle(_Angle.Type.DEG, self._value)

	class percentage(metaclass = base_type):
		def __init__(self, value):
			self._value = value

			if value < 0:
				value = 0

			# value can actually be more than 100.

		def __repr__(self):
			return f"{self._value} %"

		def to_byte(self):
			return int(min(self._value / 100, 1.0) * 255)

		def to_factor(self):
			try:
				assert 0 <= self._value <= 100
			except:
				raise ValueError("expected a value between 0.0 and 1.0, got " \
					f"{self._value}")

			return self._value / 100

	class angle(metaclass = base_type):
		def __init__(self, value):
			if not isinstance(value, _Angle):
				raise TypeError("expected an Angle instance")

			self._value = value

		def __repr__(self):
			return repr(self._value)

		def to_hue(self):
			return self._value

	class color(metaclass = base_type):
		def __init__(self, value):
			if not isinstance(value, _get_color_class()):
				raise ValueError("expected a Color instance")

			self._value = value

		def __repr__(self):
			return repr(self._value)

		def to_color(self):
			return self._value

	# ---
	# Function and named color getters.
	# ---

	def _get_functions(self):
		""" The functions getter, for getting a function using its
			name. """

		class _FunctionGetter:
			def __init__(self, ref):
				self._fref = ref

			def __getitem__(self, name):
				fref = self._fref

				# Find the method.

				if name[0:1] == '_' or name in ('functions', 'named',
					'default'):
					raise KeyError(repr(name))

				members = dict(_getmembers(fref, predicate = _ismethod))

				try:
					method = members[name]
				except (KeyError, AssertionError):
					raise KeyError(repr(name))

				# Make a function separated from the class, copy the
				# annotations and add the type check on each argument.

				class _MethodCaller:
					def __init__(self, fref, name, func):
						self._fref = fref
						self._name = name
						self._func = func

						self.__annotations__ = func.__annotations__
						try:
							del self.__annotations__['self']
						except:
							pass

						spec = _getfullargspec(func)

						def annotate(arg_name):
							try:
								return spec.annotations[arg_name]
							except:
								return None

						self._args = list(map(annotate, spec.args[1:]))
						self._optargs = self._args[-len(spec.defaults):] \
							if spec.defaults else []
						self._args = self._args[:-len(self._optargs)]

					def __call__(self, *args):
						if len(args) < len(self._args):
							raise _NotEnoughArgumentsError(len(self._args),
								self._name)
						if len(args) > len(self._args) + len(self._optargs):
							raise _TooManyArgumentsError(len(self._args),
								self._name)

						arg_types = self._args \
							+ self._optargs[:len(args) - len(self._args)]
						arg_source = args
						args = []

						lit = zip(_count(), arg_source, arg_types)
						for index, arg, exp in lit:
							args.append(arg)
							if exp is None:
								continue
							if type(arg) in exp:
								continue

							# If we haven't got a color but a color is one
							# of the accepted types, try to transform into
							# a color to manage number colors using the
							# Netscape transformation such as '123'.

							if color in exp:
								try:
									args[-1] = arg.to_color()
								except:
									pass
								else:
									continue

							raise _InvalidArgumentTypeError(index,
								exp, type(arg), self._name)

						return self._func(*args)

				return _MethodCaller(self, name, method)

		return _FunctionGetter(self)

	def _get_colors(self):
		""" The colors getter, for getting a named color. """

		class _ColorGetter:
			def __init__(self, ref):
				self._cref = ref

			def __getitem__(self, name):
				return self._cref._color(name)

		return _ColorGetter(self)

	functions = property(_get_functions)
	colors = property(_get_colors)

	# ---
	# Default methods.
	# ---

	def _color(self, name):
		""" Get a named color. """

		raise KeyError(f'{name}: no such color')

	def default():
		""" Get the default reference. """

		global _default_reference

		if _default_reference is not None:
			return _default_reference

		from ._builtin import DefaultReference
		_default_reference = DefaultReference()
		return _default_reference

# End of file.
