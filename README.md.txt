# Resolution Theorem Prover
* written in Python

# Author
* Nonso Iwu

A Theorem can take a number of Axioms in clausal form as its
premises (Knowledge Base) and its goals.

These Axioms contain 0 or more Predicates.

The Theorem attempts to derive the 'Ø' clause (clause with 0 predicates) by resolving each Axiom within its goals set against those in the premises set.

Predicate examples:
	(grandparent ?x ?y)
	(parent ?x ?y)
	(parent ?x Sue)
	~(parent Doug ?y)

where '?' denotes a variable and '~' denotes negation.

Axiom example:
	[(grandparent ?x ?y) ~(parent ?x ?z) ~(parent ?z ?y)]

which reads:
If x is the grandparent of y then x is the parent of z and z is the parent of y.

Moreover...
Axioms are horn clauses. This means that the axiom shown above entails:

(grandparent ?x ?y) => (parent ?x ?z) and (parent ?z ?y)

which is equivalent to:
(grandparent ?x ?y) or ~(parent ?x ?z) ~(parent ?z ?y)

# How to use

The Theorem Prover corresponds to the ```Theorem``` class (in theorem_prover.py)

A ```Theorem``` class contains ```Axiom``` classes within it's ```goals``` and ```premises``` lists.
An ```Axiom``` class contains ```Predicates``` classes
And a ```Predicate``` class contains ```pElement``` classes

The following lines generates a ```pElement``` class:
```
pElem1 = pElement().setAttributes("name1", "?")
pElem2 = pElement().setAttributes("name2", "c")
```
where ```pElem1``` is a variable (w/ "?" passed in to the second argument of pElement.setAttributes()) named 'name1'
and ```pEleme2``` is a constant (w/ "c" passed in to the second argument of ```pElement.setAttributes()```) named 'name2'

The following lines generates a ```Predicate``` class:	
```
pred1 = Predicate().setAttributes("pred1", [pElem1, pElem2])
pred2 = Predicate().setAttributes("pred2", [pElem2])
```
where ```pred1``` will read, (pred1 ?name1 name2)
and ```pred2``` will read, (pred2 name2)

The following lines generates an ```Axiom``` class:	
```
ax1 = Axiom().setAttributes([pred1])
ax2 = Axiom().setAttributes([pred2])
```
where ```ax1``` will read, ((pred1 ?name1 name2), (pred2 name2)), 
and ```ax2``` will read, ((pred2 name2))

And finally, the following lines will generates a ```Theorem``` class:
```
th = Theorem().setAttributes([ax2],[ax1])
```
The ```goals``` and ```premises``` attributes of a ```Theorem``` class will be set to the first and second arguments of ```Theorem.setAttributes()``` respectively.

In order to run the Resolution Theorem Solver on a given Theorem, the ```Theorem``` class has the method ```Theorem.prove()```

This line will run a Depth First Search on a ```Theorem``` class:
```
th.prove()
``` 
and print the output while also returning a list of bindings for resolution.

In order to run a Breadth First Search, the ```searchType``` attribute of a ```Theroem``` class must be set to ```True```.

This line will run a Breadth First Search on a ```Theorem``` class:
```
th.setSearch(True).prove()
```

# Notes

Source code:
```
theorem_prover.py
```

Tests for module functionality: 
```
theorem_prover_tests.py
```

Tests for ```Theorem``` class (derived from 'test-prover.txt'):
```
test_prover.py
```