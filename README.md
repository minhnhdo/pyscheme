# A subset of scheme #
    Inspiration drawn much from The Little Schemer by Daniel P. Friedman and Mathias Felleisen

# Currently working features: #
+ Truth values, i.e. #t and #f
+ Numbers, i.e. integers and floats
+ Atoms (as strings)
+ Lists (as Python lists)
+ Primitive functions/forms:
    + Additions (+ &lt;arg1&gt; &lt;arg2&gt; ...) implemented with the sum function
    + Products (\* &lt;arg1&gt; &lt;arg2&gt; ...)
    + Quotes (quote &lt;arg&gt;)
    + Lambdas (lambda (&lt;arglist&gt;) &lt;sexp&gt;)

# Notes #
1. Currently, the number of provided arguments isn't checked, except for lambdas (which will raise a TypeError). Thus,  
        (quote a b) --&gt; 'a'
2. The bodies of lambdas only accept one s-expression each (this can be fixed, temporarily, with a begin function). Therefore,  
        ((lambda (x) (+ x 1) (- x 5)) 5) -&gt; 6
3. Because of Python's duck typing, this is possible:  
        (* 'a' (quote 2)) --&gt; 'aa'
