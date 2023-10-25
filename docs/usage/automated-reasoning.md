# Automated Reasoning

Mathesis provides simple solvers (reasoners, provers) based on truth table method and on tableau method.

## Reasoning in propositional logic

### Solvers based on truth table method

See [Truth tables](truth-tables.md).

### Solvers based on tableau method

`mathesis.solvers.ClassicalSolver` is a solver for classical propositional logic based on tableau method.

```python exec="1" result="text" source="above"
from mathesis.grammars import BasicGrammar
from mathesis.solvers import ClassicalSolver

grammar = BasicGrammar()

fml = grammar.parse("((A → B)∧(A → C)) → (A → (B∧C))")
sol = ClassicalSolver().solve([], [fml])

print(sol.htree())
print(f"Valid: {sol.is_valid()}")
```