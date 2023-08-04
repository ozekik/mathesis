# Proofs with Tableaux

<a href="https://en.wikipedia.org/wiki/Method_of_analytic_tableaux" target="_blank">Semantic tableau</a> (plural: tableaux) is a decision/proof procedure for propositional and quantified logics.

## Unsigned tableaux

`mathesis.deduction.tableau.Tableau` is a class for unsigned tableaux.
It is initialized with an inference, given as a list of premises and of conclusions.

```python exec="1" result="text" source="above"
from mathesis.grammars import BasicGrammar
from mathesis.deduction.tableau import Tableau

grammar = BasicGrammar()

premises = grammar.parse(["A→B", "B→C"])
conclusions = grammar.parse(["A→C"])
tab = Tableau(premises, conclusions)

print(tab.htree())
```

A tableau is a tree of nodes, each node being a formula.
Mathesis automatically indexes the nodes, so that you can access them by their index.
You can apply a rule to a node of tableau with `tab.apply(node, rule)` where `tab` is a tableau:

```python exec="1" result="text" source="above"
from mathesis.grammars import BasicGrammar
from mathesis.deduction.tableau import Tableau, rules

grammar = BasicGrammar()

premises = grammar.parse(["A→B", "B→C"])
conclusions = grammar.parse(["A→C"])
tab = Tableau(premises, conclusions)

print(tab.htree())
print(f"Closed: {tab.is_closed()}\n")

tab.apply(tab[3], rules.NegatedConditionalRule())
print(tab.htree())
tab.apply(tab[1], rules.ConditionalRule())
print(tab.htree())
tab.apply(tab[2], rules.ConditionalRule())
print(tab.htree())

print(f"Closed: {tab.is_closed()}")
```

A branch is a path from the root to a leaf of the tableau.
A branch is closed if it contains a contradiction (i.e., contradictory formulas.)
The tableau is closed if all branches are closed.

## Signed tableaux

A signed tableau is a tableau where each node is signed with a truth value.

```python exec="1" result="text" source="above"
from mathesis.grammars import BasicGrammar
from mathesis.deduction.tableau import SignedTableau, signed_rules

grammar = BasicGrammar()

premises = grammar.parse(["A→B", "B→C"])
conclusions = grammar.parse(["A→C"])
tab = SignedTableau(premises, conclusions)

print(tab.htree())
```

## Further reading

See [Automated reasoning](automated-reasoning.md) for automated reasoning with tableaux.
