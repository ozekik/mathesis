# Truth tables

## Show truth tables for the connectives

Truth functions are defined as "clauses" and can be printed as truth tables.

```python exec="1" result="text" source="above"
from mathesis.system.classical.truth_table import ConditionalClause

conditional_clause = ConditionalClause()

print(conditional_clause)
```

## Generate truth tables for classical logic

`mathesis.semantics.truth_table.ClassicalTruthTable` generates the truth table for a given formula.

```python exec="1" result="text" source="above"
from mathesis.grammars import BasicGrammar
from mathesis.semantics.truth_table import ClassicalTruthTable

grammar = BasicGrammar()

fml = grammar.parse("(¬P∧(P∨Q))→Q")

table = ClassicalTruthTable(fml)
print(table)

print(f"Valid: {table.is_valid()}")
```

## Generate truth tables for many-valued logics

WIP

## Show tables as HTML (JupyerLab/Jupyter Notebook)

WIP
