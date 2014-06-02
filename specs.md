valid forms:
	(define symbol value)
	(lambda (args...) body)
	(begin exprs...)
	(if conditional then else)
	(function args...)
	
functions:
	numeric:
		+, -, /, *, pow, abs, mod
	comparators:
		=, !=, >, <, >=, <=
	boolean:
		not, or, and
	identity:
		equal?
	list:
		list, cons, car, cdr
	
tokens:
	integers
	floats
	strings
	symbols
	boolean