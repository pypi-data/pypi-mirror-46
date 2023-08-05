#!/usr/bin/env python3
#******************************************************************************
# Copyright (C) 2019 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the thcolor project, which is MIT-licensed.
#******************************************************************************
""" Exception definitions, with internal and external exceptions defined. """

__all__ = ["ColorExpressionDecodingError",
	"NotEnoughArgumentsError", "TooManyArgumentsError",
	"InvalidArgumentTypeError", "InvalidArgumentValueError"]

# ---
# External exceptions.
# ---

class ColorExpressionDecodingError(Exception):
	""" A color decoding error has occurred on the text. """

	def __init__(self, text, column = None, func = None):
		self._column = column
		self._func = func
		self._text = text

	def __str__(self):
		msg = ""

		if self._column is not None:
			msg += f"at column {self._column}"
			if self._func is not None:
				msg += ", "
		if self._func is not None:
			msg += f"in function {repr(self._func)}"
		if msg:
			msg += ": "

		return msg + self._text

# ---
# Internal exceptions.
# ---

class NotEnoughArgumentsError(Exception):
	""" Not enough arguments. """

	def __init__(self, count, name = None):
		self._name = name
		self._count = count

	def __str__(self):
		msg = "not enough arguments"
		if self._name is not None:
			msg += f" for function {repr(self._name)}"
		msg += f", expected {self._count} arguments at least"

		return msg

	@property
	def count(self):
		return self._count

class TooManyArgumentsError(Exception):
	""" Too many arguments. """

	def __init__(self, count, name = None):
		self._name = name
		self._count = count

	def __str__(self):
		msg = "too many arguments"
		if self._name is not None:
			msg += f" for function {repr(self._name)}"
		msg += f", expected {self._count} arguments at most"

		return msg

	@property
	def count(self):
		return self._count

class InvalidArgumentTypeError(Exception):
	""" Invalid argument type. """

	def __init__(self, index, expected, got, name = None):
		self._name = name
		self._index = index
		self._expected = expected
		self._got = got

	def __str__(self):
		msg = f"wrong type for argument {self._index + 1}"
		if self._name:
			msg += f" of function {repr(self._name)}"
		msg += f": expected {self._expected}, got {self._got}"

		return msg

	@property
	def index(self):
		return self._index

	@property
	def expected(self):
		return self._expected

	@property
	def got(self):
		return self._got

class InvalidArgumentValueError(Exception):
	""" Invalid argument value. """

	def __init__(self, index, text, name = None):
		self._name = name
		self._index = index
		self._text = text

	def __str__(self):
		msg = f"erroneous value for argument {self._index + 1}"
		if self._name:
			msg += f" of function {repr(self._name)}"
		msg += f": {self._text}"

		return msg

	@property
	def index(self):
		return self._index

	@property
	def text(self):
		return self._text

# End of file.
