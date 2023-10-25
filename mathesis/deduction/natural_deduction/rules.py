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
        def __init__(self):
            pass

        def apply(self, target, tip, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Sign is not positive"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"
            antec, conseq = target.fml.subs

            # TODO: Better way to check conditions
            premises = list(map(lambda x: str(x.fml), target.sequent_node.sequent.left))
            # print(premises)
            assert str(antec) in premises, "Antecendent does not match"

            # conclusion = str(target.sequent_node.sequent.right[0].fml)
            # print(conclusion)
            # assert str(conseq) == conclusion, "Consequent does not match"

            node2 = Node(
                str(conseq), sign=sign.POSITIVE, fml=conseq, parent=tip, n=next(counter)
            )
            return {
                "queue_items": [[node2]],
                "counter": counter,
            }
