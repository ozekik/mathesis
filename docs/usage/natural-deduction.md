# Proofs using Natural Deduction

## Introduction

In mathesis, a state of a natural deduction proof and its subproofs consists of the (sub)proof's available premises and conclusion at a step.
A state is displayed as `<premises> ⇒ <conclusion>`.
Intuitively, the formulas on the left side of `⇒` are what to come to the upper part of the final (sub)proof, and those on the right side of `⇒` are what to come to the lower part of the final (sub)proof.

Natural deduction is a proof system that consists of elimination rules and introduction rules. In mathesis,

- you can apply an **elimination rule** *up-to-down* to the premises of a (sub)proof to obtain new premises.
- Similarly, you can apply an **introduction rule** *down-to-up* to the conclusion of a (sub)proof and convert it into new subproofs.

```python exec="1" result="text" source="above"
from mathesis.grammars import BasicGrammar
from mathesis.deduction.natural_deduction import NDTree, rules

grammar = BasicGrammar()

premises = grammar.parse(["A∨B", "B→C"])
conclusion = grammar.parse("A∨C")
deriv = NDTree(premises, conclusion)
print(deriv.tree())

deriv.apply(deriv[1], rules.Disjunction.Elim())
print(deriv.tree())

deriv.apply(deriv[7], rules.Disjunction.Intro("left"))
print(deriv.tree())

deriv.apply(deriv[8], rules.Conditional.Elim())
print(deriv.tree())

deriv.apply(deriv[16], rules.Disjunction.Intro("right"))
print(deriv.tree())
```

## Render as Gentzen-style Proof

WIP

## Render as Fitch-style Proof

WIP

## Render as Suppes-Lemmon-style Proof

WIP

## Render as Sequent Calculus Proof

WIP
