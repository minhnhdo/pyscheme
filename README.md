# A subset of scheme #
Inspiration drawn much from The Little Schemer by Daniel P. Friedman and Mathias Felleisen

# Currently working features: #
+ Truth values, i.e. #t and #f
+ Numbers, i.e. integers and floats
+ Atoms (as strings)
+ Lists (as Python lists)
+ Primitive functions/forms:
    + Additions (+ &lt;arg1&gt; &lt;arg2&gt; ...) implemented with the sum function
    + Multiplications (\* &lt;arg1&gt; &lt;arg2&gt; ...)
    + Difference (\* &lt;arg1&gt; &lt;arg2&gt; ...) which takes at least 1 argument
    + Divisions (/ &lt;arg1&gt; &lt;arg2&gt; ...) which takes at least 1 argument
    + Quotes (quote &lt;arg&gt;)
    + Begins (begin &lt;arg1&gt; &lt;arg2&gt; ...) which will return the value of the last s-expression
    + Lambdas (lambda (&lt;arglist&gt;) &lt;sexps&gt;)
    + Conditions (cond (&lt;cond1&gt; &lt;sexps1&gt;) (&lt;cond1&gt; &lt;sexps1&gt;) ...)

# Notes #
1. Currently, the number of provided arguments isn't checked, except for lambdas (which will raise a TypeError), division along with difference (which demands at least 1 argument and will also raise a TypeError if this is not met). Thus,  

        (quote a b) --> 'a'
        (/) --> TypeError: Expected at least 1 arguments (0 provided)
2. Because of Python's duck typing, this is possible:  

        (* 2 (quote a)) --> 'aa'
