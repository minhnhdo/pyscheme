# A subset of scheme #
Inspiration drawn much from The Little Schemer by Daniel P. Friedman and Mathias Felleisen

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

            (+ &lt;arg1&gt; &lt;arg2&gt; ...)
    + Multiplications:

            (\* &lt;arg1&gt; &lt;arg2&gt; ...)
    + Difference which takes at least 1 argument:

            (\* &lt;arg1&gt; &lt;arg2&gt; ...)
    + Divisions which takes at least 1 argument:

            (/ &lt;arg1&gt; &lt;arg2&gt; ...)
    + Predicates: &gt;, &lt;, =, not, eq?, null?, atom?, zero?
    + Connectives: and, or
    + Quotes

            (quote &lt;arg&gt;)
    + Begins which will evaluate to the value of the last s-expression:

            (begin &lt;arg1&gt; &lt;arg2&gt; ...)
    + Lambdas

            (lambda (&lt;arglist&gt;) &lt;sexps&gt;)
    + Conditions

            (cond (&lt;cond1&gt; &lt;sexps1&gt;) (&lt;cond1&gt; &lt;sexps1&gt;) ...)

# Notes #
1. Currently, the number of provided arguments isn't checked, except for lambdas (which will raise a TypeError). Thus,

        (quote a b) --> 'a'
        (/) --> TypeError: Expected at least 1 arguments (0 provided)
2. Because of Python's duck typing, this is possible:  

        (* 2 (quote a)) --> 'aa'
