#JCLI DOCUMENTATION

##Functions

###Numerics Operators

* `(+ numbers ...)` -> number
   * returns the sum of exprs
* `(- numbers ...)` -> number
   * if called with one argument, returns the negation of exprs
   * otherwise, returns the difference between the first argument and the sum of the other arguments
* `(* numbers ...)` -> number
   * returns the product of exprs
* `(/ number ...)` -> number
   * if called with one argument, return the reciprocal of exprs
   * otherwise, returns the quotient of the first argument and the product of the other arguments
* `(expt base exponent modulus?)` -> number
   * if called with two arguments, returns base^exponent
   * if called with three arguments, return base^exponent (mod modulus)
* `(abs number)` -> number
   * returns the absolute value of number
* `(modulo number modulus)`
   * returns number (mod modulus)

###Comparators

* `(= exprs ...)` -> bool
   * returns true if all exprs are equal, false otherwise
* `(!= expr0 expr1)` -> bool
   * equivalent to (not (= expr0 expr1))
* `(> exprs ...)` -> bool
   * returns true if arguments in the given order are strictly decreasing, false otherwise
* `(< exprs ...)` -> bool
   * returns true if arguments in the given order are strictly increasing, false otherwise
* `(>= exprs ...)` -> bool
   * returns true if arguments in the given order are non-increasing, false otherwise
* `(<= exprs ...)` -> bool
   * returns true if arguments in the given order are non-decreasing, false otherwise
* `(equal? exprs ...)` -> bool
   * returns true if all exprs reference the same object, false otherwise

###Boolean Operators

* `(not expr)` -> bool
   * returns true if expr is false, false otherwise
* `(or exprs ...)` -> bool
   * returns true if any exprs are true, false otherwise
* `(and exprs ...)` -> bool
   * returns true if all exprs are equal, false otherwise

###List Operators

* `(list exprs ...)` -> list
   * returns a list containing exprs in the given order
* `(car list)` -> expr
   * returns the first element of list
* `(cdr list0)` -> list
   * returns a list containing all the elements of list0 in order, except for the first element
* `(cons expr list0)` -> list
   * returns the list resulting from prepending expr to list0
* `(length list)` -> number
   * returns the length of the list
* `null`
   * the empty list



















