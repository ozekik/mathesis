from itertools import count
from typing import Literal
from anytree import Node
from mathesis.deduction.tableau import signed_rules, sign
from mathesis import forms

Rule = signed_rules.Rule


class Negation:
    Intro = signed_rules.NegativeNegationRule
    Elim = signed_rules.PositiveNegationRule


class Conjunction:
    Intro = signed_rules.NegativeConjunctionRule
    # TODO: Choice of conjunct
    Elim = signed_rules.PositiveConjunctionRule


class Disjunction:
    # Intro = signed_rules.NegativeDisjunctionRule
    class Intro(Rule):
        def __init__(self, disjunct: Literal["left", "right"]):
            self.disjunct = disjunct

        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Sign is not negative"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"
            disj1, disj2 = target.fml.subs
            node1 = Node(
                str(disj1), sign=sign.NEGATIVE, fml=disj1, parent=tip, n=next(counter)
            )
            node2 = Node(
                str(disj2), sign=sign.NEGATIVE, fml=disj2, parent=node1, n=next(counter)
            )

            if self.disjunct == "left":
                node = node1
            elif self.disjunct == "right":
                node = node2

            return {
                "queue_items": [[node]],
                "counter": counter,
            }

    Elim = signed_rules.PositiveDisjunctionRule


class Conditional:
    Intro = signed_rules.NegativeConditionalRule

    class Elim(Rule):
        def __init__(self, antecendent):
            self.antecendent = antecendent

        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Sign is not positive"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"
            antec, desc = target.fml.subs
            print(str(antec), str(self.antecendent.fml))
            assert str(antec) == str(self.antecendent.fml), "Antecendent does not match"
            node2 = Node(
                str(desc), sign=sign.POSITIVE, fml=desc, parent=tip, n=next(counter)
            )
            return {
                "queue_items": [[node2]],
                "counter": counter,
            }
