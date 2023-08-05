#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Angle management. """

from math import pi as _pi
from enum import Enum as _Enum

__all__ = ["Angle"]

def _deg(name, value):
	value = float(value)
	return value # % 360.0

def _grad(name, value):
	value = float(value)
	return value # % 400.0

def _rad(name, value):
	value = float(value)
	return value # % (2 * _pi)

def _turn(name, value):
	value = float(value)
	return value # % 1

# ---
# Angle definition.
# ---

class _AngleType(_Enum):
	""" The angle unit type. """

	""" Invalid angle. """
	INVALID = 0

	""" Degrees (360 degrees in a full circle). """
	DEG = 1

	""" Gradiants (400 gradiants in a full circle). """
	GRAD = 2

	""" Radiants (2π radiants in a full circle). """
	RAD = 3

	""" Turns (1 turn in a full circle). """
	TURN = 4

class Angle:
	""" Represent an angle with all of its available formats. """

	# Properties to work with:
	#
	# `_type`: the type as one of the `Angle.Type` constants.
	# `_value`: the angle value.

	Type = _AngleType

	def __init__(self, *args, **kwargs):
		self._type = Angle.Type.INVALID
		self.set(*args, **kwargs)

	def __repr__(self):
		args = (('type', self._type),)
		if self._type in (Angle.Type.DEG, Angle.Type.GRAD, Angle.Type.RAD,
			Angle.Type.TURN):
			args += (('value', self._value),)

		argtext = ', '.join(f'{key}: {repr(value)}' for key, value in args)
		return f"{self.__class__.__name__}({argtext})"

	# ---
	# Management methods.
	# ---

	def set(self, *args, **kwargs):
		""" Set the angle. """

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
				if type == Angle.Type.INVALID:
					raise TypeError(f"{self.__class__.__name__}() missing " \
						"required argument: 'type'")

		try:
			type = Angle.Type(type)
		except:
			type = Angle.Type.DEG

		# Initialize the properties.

		if   type == Angle.Type.DEG:
			self._value, = _decode_varargs(\
				(('value', 'angle', 'degrees'), _deg))
		elif type == Angle.Type.GRAD:
			self._value, = _decode_varargs(\
				(('value', 'angle', 'gradiants'), _grad))
		elif type == Angle.Type.RAD:
			self._value, = _decode_varargs(\
				(('value', 'angle', 'radiants'), _rad))
		elif type == Angle.Type.TURN:
			self._value, = _decode_varargs(\
				(('value', 'angle', 'turns'), _turn))
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
	def degrees(self):
		""" Get the angle in degrees. """

		return self.turns * 360

	@property
	def gradiants(self):
		""" Get the angle in gradiants. """

		return self.turns * 400

	@property
	def radiants(self):
		""" Get the angle in radiants. """

		return self.turns * (2 * _pi)

	@property
	def turns(self):
		""" Get the angle in turns. """

		if   self._type == Angle.Type.DEG:
			return self._value / 360
		elif self._type == Angle.Type.GRAD:
			return self._value / 400
		elif self._type == Angle.Type.RAD:
			return self._value / (2 * _pi)
		elif self._type == Angle.Type.TURN:
			return self._value

# End of file.
