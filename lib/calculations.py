import re, textwrap
from enum import Enum
from typing import List, Union 
from sympy import Integer, Symbol, Eq, solve, Rational, sympify, Float, simplify, powsimp
from sympy.parsing.sympy_parser import implicit_multiplication_application, standard_transformations, parse_expr
from .numbers import int_if_dotzero_float, to_superscript, quadratic_to_superscript

transformations = (standard_transformations + (implicit_multiplication_application,))

def equate(string: str):
	string = string.lower().replace('^', '**')
	arr = re.findall("[a-z]", string)
	env = {
	    'solve': solve,
	    'Eq': Eq
	}
	if len(arr) > 0 and '=' in string:
		equation = str(parse_expr(string.split('=')[0], transformations=transformations))
		result = string.split('=')[1]
		for l in arr:
			env[l] = Symbol(l, real=True)
		funcdef = f"def _solve_equation():\n{textwrap.indent(f'return solve(Eq({equation}, {result}))', '   ')}"
		try:
			exec(funcdef, env)
			res = env['_solve_equation']()
			if isinstance(res, Rational):
				return f'{float(res)} ({res})'
			elif isinstance(res, List):
				if len(res) >= 2:
					return res
				else:
					if isinstance(res[0], Integer):
						return format(res[0])
					elif isinstance(res[0], Rational):
						return f'{Float(res[0])} ({res[0]})'
					else:
						return format(sympify(res[0]).evalf())
			else:
				return 0;
		except Exception as e:
			return e
	else:
		return 0;

class sequence_types(Enum):
	arithmetic = 0
	geometric = 1
	quadratic = 2
	fibonacci = 3
	unknown = 5 

def determine_sequence_type(terms: List[Union[int, float]]):
	first_diff = []
	second_diff = []
	for i in range(0, len(terms) - 1):
		ft = terms[i]
		st = terms[i + 1]
		first_diff.append(max([ft, st]) - min([ft, st]))

	for i in range(len(first_diff) - 1, 0, -1):
		ft = first_diff[i]
		st = first_diff[i - 1]
		second_diff.append(max([ft, st]) - min([ft, st]))

	if len(first_diff) == len(terms) - 1:
		if first_diff.count(first_diff[0]) == len(first_diff):
			return sequence_types.arithmetic
		elif second_diff.count(second_diff[0]) == len(second_diff):
			return sequence_types.quadratic
		else:
			first_diff_geometric_possible = []
			for i in range(0, len(terms) - 1):
				ft = terms[i]
				st = terms[i + 1]
				first_diff_geometric_possible.append(int_if_dotzero_float(st / (ft if ft > 0 else 1)))
			if first_diff_geometric_possible.count(first_diff_geometric_possible[0]) == len(first_diff_geometric_possible):
				return sequence_types.geometric
			else:
				products_potenial_fibonacci = []
				for i in list(map(lambda t: terms.index(t), terms)):
					if i < 1 or i + 1 > len(terms) - 1:
						continue
					st = terms[i - 1]
					ft = terms[i]
					products_potenial_fibonacci.append(st + ft == terms[i + 1])
				if all(products_potenial_fibonacci):
					return sequence_types.fibonacci
	return sequence_types.unknown

def get_nth_term(terms: List[Union[int, float]], seq_type: sequence_types):
	if seq_type is sequence_types.arithmetic:
		first_diff = []
		for i in range(0, len(terms) - 1):
			ft = terms[i]
			st = terms[i + 1]
			first_diff.append(max([ft, st]) - min([ft, st]))
		a = terms[0]
		d = first_diff[0]
		return format(simplify(simplify(parse_expr(f'{a} + {d}n + {d}*-1', transformations=transformations))))
	elif seq_type is sequence_types.geometric:
		first_diff_geometric_possible = []
		for i in range(0, len(terms) - 1):
			ft = terms[i]
			st = terms[i + 1]
			first_diff_geometric_possible.append(int_if_dotzero_float(st / (ft if ft > 0 else 1)))
		a = terms[0]
		r = first_diff_geometric_possible[0]
		tN = powsimp(parse_expr(f'{a} * {r}**(n-1)', transformations=transformations))
		return to_superscript(re.sub(r'\(|\)', '', str(tN).replace('**', '^').replace(' ', ''), 0, re.MULTILINE))
	elif seq_type is sequence_types.quadratic:
		first_diff = []
		second_diff = []
		for i in range(0, len(terms) - 1):
			ft = terms[i]
			st = terms[i + 1]
			first_diff.append(max([ft, st]) - min([ft, st]))

		for i in range(len(first_diff) - 1, 0, -1):
			ft = first_diff[i]
			st = first_diff[i - 1]
			second_diff.append(max([ft, st]) - min([ft, st]))

		a = equate(f'2a={second_diff[0]}')
		b = equate(f'(3*{a})+b={first_diff[0]}')
		c = equate(f'{a}+{b}+c={terms[0]}')
		tN = simplify(parse_expr(f'({a}n**2)+({b}n)+{c}', transformations=transformations))
		return quadratic_to_superscript(str(tN).replace('**', '^')).replace('^', '')
	elif seq_type is sequence_types.fibonacci:
		return 'Tn-1 + Tn-2'
	else:
		seq_type = determine_sequence_type(terms)
		if seq_type == sequence_types.unknown:
			return None
		else:
			get_nth_term(terms, seq_type)


def beautify_sympy(s: str, sequence_type: sequence_types = sequence_types.unknown):
	if '*' in s:
		s = s.replace('*', '')

	return s