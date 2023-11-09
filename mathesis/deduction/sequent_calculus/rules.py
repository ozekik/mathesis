from itertools import count

from mathesis import forms
from mathesis.deduction.sequent_calculus.sequents import Sequent, SequentItem, sign


class Rule:
    pass


class StructuralRule(Rule):
    pass


def _apply(target, new_items, counter):
    branch_items = new_items

    for item in target.sequent.items:
        if item != target:
            node = item.clone()
            node.n = next(counter)
            branch_items.append(node)

    branch_sequent = Sequent([], [], parent=target.sequent)
    branch_sequent.items = branch_items

    return branch_sequent


class Negation:
    # Left = signed_rules.PositiveNegationRule
    class Left(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Not on the left side of sequent"
            assert isinstance(target.fml, forms.Negation), "Not a negation"

            subfml = target.fml.sub
            new_item = SequentItem(subfml.clone(), sign.NEGATIVE, n=next(counter))
            branch_sequent = _apply(target, [new_item], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }

    # Right = signed_rules.NegativeNegationRule
    class Right(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Not on the right side of sequent"
            assert isinstance(target.fml, forms.Negation), "Not a negation"

            subfml = target.fml.sub
            new_item = SequentItem(subfml.clone(), sign.POSITIVE, n=next(counter))
            branch_sequent = _apply(target, [new_item], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }


class Conjunction:
    # Left = signed_rules.PositiveConjunctionRule
    class Left(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Not on the left side of sequent"
            assert isinstance(target.fml, forms.Conjunction), "Not a conjunction"

            conj1, conj2 = target.fml.subs
            conj1 = SequentItem(conj1.clone(), sign.POSITIVE, n=next(counter))
            conj2 = SequentItem(conj2.clone(), sign.POSITIVE, n=next(counter))
            branch_sequent = _apply(target, [conj1, conj2], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }

    # Right = signed_rules.NegativeConjunctionRule
    class Right(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Not on the right side of sequent"
            assert isinstance(target.fml, forms.Conjunction), "Not a conjunction"

            branches = []

            for conj in target.fml.subs:
                conj = SequentItem(conj.clone(), sign.NEGATIVE, n=next(counter))
                branch_sequent = _apply(target, [conj], counter)
                branches.append(branch_sequent)

            return {
                "queue_items": branches,
                "counter": counter,
            }


class Disjunction:
    # Left = signed_rules.PositiveDisjunctionRule
    class Left(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Not on the left side of sequent"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"

            branches = []

            for subfml in target.fml.subs:
                new_item = SequentItem(subfml.clone(), sign.POSITIVE, n=next(counter))
                branch_sequent = _apply(target, [new_item], counter)
                branches.append(branch_sequent)

            return {
                "queue_items": branches,
                "counter": counter,
            }

    # Right = signed_rules.NegativeDisjunctionRule
    class Right(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Not on the right side of sequent"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"

            disj1, disj2 = target.fml.subs
            disj1 = SequentItem(disj1.clone(), sign.NEGATIVE, n=next(counter))
            disj2 = SequentItem(disj2.clone(), sign.NEGATIVE, n=next(counter))
            branch_sequent = _apply(target, [disj1, disj2], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }


class Conditional:
    # Left = signed_rules.PositiveConditionalRule
    class Left(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Not on the left side of sequent"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"

            antec, conseq = target.fml.subs
            antec = SequentItem(antec.clone(), sign.NEGATIVE, n=next(counter))
            branch_sequent_1 = _apply(target, [antec], counter)
            conseq = SequentItem(conseq.clone(), sign.POSITIVE, n=next(counter))
            branch_sequent_2 = _apply(target, [conseq], counter)

            return {
                "queue_items": [branch_sequent_1, branch_sequent_2],
                "counter": counter,
            }

    # Right = signed_rules.NegativeConditionalRule
    class Right(Rule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Not on the right side of sequent"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"

            antec, conseq = target.fml.subs
            antec = SequentItem(antec.clone(), sign.POSITIVE, n=next(counter))
            conseq = SequentItem(conseq.clone(), sign.NEGATIVE, n=next(counter))
            branch_sequent = _apply(target, [antec, conseq], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }


class Weakening:
    class Left(StructuralRule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Not on the left side of sequent"

            branch_sequent = _apply(target, [], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }

    class Right(StructuralRule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Not on the right side of sequent"

            branch_sequent = _apply(target, [], counter)

            return {
                "queue_items": [branch_sequent],
                "counter": counter,
            }


class Contraction:
    # TODO
    pass


class Exchange:
    # TODO
    pass
