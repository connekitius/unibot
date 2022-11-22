import re, math
from typing import Union, Callable

def to_superscript_translation(num: re.Match):
	return num[0].replace('^', '').translate(str.maketrans(dict(zip('1234567890n-+', '¹²³⁴⁵⁶⁷⁸⁹⁰ⁿ⁻⁺'))))

def to_superscript(s: str):
	s = s.replace(' ', '')
	res = re.finditer(r'\^\s*(\d+)?((n)?(\+\d+)|(n)?(-\d+))', s, re.MULTILINE)
	return to_superscript_translation(list(res)[0])

def quadratic_to_superscript(s: str):
	return re.sub(r'\^\s*(\d+)', to_superscript_translation, s, 0, re.MULTILINE)

int_if_dotzero_float: Callable[[Union[int, float, str]], Union[int, float]] = lambda i: round(float(i)) if float(i) % (math.floor(float(i)) if math.floor(float(i)) > 0 else 1) == 0 else float(i)