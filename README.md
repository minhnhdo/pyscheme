# A subset of scheme #
Inspiration drawn much from The Little Schemer by Daniel P. Friedman and Mathias Felleisen

# What is does #
This little Python program tries to evaluate Scheme (a Lispy language) code.
When run using ```python scheme.py```, it provides a (rudimentary) Read-Eval-Print Loop.

# Currently working features: #
+ Truth values, i.e. #t and #f
+ Numbers, i.e. integers and floats
+ Atoms (as strings)
+ Lists (as Python lists)
+ Primitive functions/forms:
    + List manipulation:

            (cons a b)
            (car l)
            (cdr l)
    + Additions implemented with the sum function:

            (+ <arg1> <arg2> ...)
    + Multiplications:

            (* <arg1> <arg2> ...)
    + Difference which takes at least 1 argument:

            (- <arg1> <arg2> ...)
    + Divisions which takes at least 1 argument:

            (/ <arg1> <arg2> ...)
    + Predicates: &gt;, &lt;, =, not, eq?, null?, atom?, zero?
    + Connectives: and, or
    + Quotes

            (quote <arg>)
            '<arg>
    + Begins which will evaluate to the value of the last s-expression:

            (begin <arg1> <arg2> ...)
    + Lambdas

            (lambda (<arglist>) <sexps>)
    + Conditions

            (cond (<cond1> <sexps1>) (<cond1> <sexps1>) ...)

# Notes #
1. Currently, the number of provided arguments isn't checked, except for lambdas (which will raise a TypeError). Thus,

        (quote a b) --> 'a'
        (/) --> TypeError: Expected at least 1 arguments (0 provided)
2. Because of Python's duck typing, this is possible:  

        (* 2 (quote a)) --> 'aa'
