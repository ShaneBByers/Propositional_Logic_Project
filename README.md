Shane Byers

CMPSC 442 (Artificial Intelligence Course) Project 4: Implement a program that demonstrates the manipulation of propositional logic statements.

11/16/2016

TO RUN: 
>  python -i propositional_logic.py
>  Create a propositional logic statement using:
>>    Atom("variable_name")

>>    Not(Expression)

>>    And(Expression)

>>    Or(Expression)

>>    Implies(Expression)

>>    Iff(Expression)

>  Convert statement to Conjunctive Normal Form (CNF):
>>    statement_variable.to_cnf()

>  Evaluate expression with assignments:
>>    statement_variable.evaluate(assignment) -- Assignment is a dictionary mapping atom variable names to either True or False

>  Find all satisfying assignments:
>>    satisfying_assignments(statement_variable)
    
EXAMPLE:
>  python -i propositional_logic.py

>  a = Atom("a")

>  b = Atom("b")

>  c = Atom("c")

>  statement = Implies(And(a,b),Not(c))

>  statement.to_cnf()

>  assignment = {"a":True,"b":False,"c":False}

>  statement.evaluate(assignment)

>  satisfying_assignments(statement)
  
This program is a simple program that shows the possibilities for manipulating propositional logic statements and how a computer may go about doing so on a lower level. Understanding how propositional logic statements work is crucial for any form of Computer Science, but especially for some branches of Artificial Intelligence.
    
  

KNOWN ISSUES:

There may be an issue with to_cnf on the more complex statements that could exist.

It may also be worth it to look into a better way of inputting a statement if the user desires. It may also be worth it to display the statements in a more easy-to-understand manner to allow for easier to read results.
