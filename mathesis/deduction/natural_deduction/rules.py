from copy import deepcopy
from itertools import count
from typing import Literal

from mathesis import forms
from mathesis.deduction.natural_deduction.natural_deduction import NDSubproof
from mathesis.deduction.sequent_calculus import Sequent, SequentItem
from mathesis.deduction.tableau import sign


def _apply(target, new_items, counter, preserve_target=True):
    branch_items = new_items
    new_target = None

    for item in target.sequent.items:
        if item != target or preserve_target:
            node = item.clone()
            node.n = next(counter)
            if item == target:
                new_target = node
            branch_items.append(node)

    branch_sequent = Sequent([], [], parent=target.sequent)
    branch_sequent.items = branch_items

    if preserve_target:
        return branch_sequent, target
    else:
        return branch_sequent


class Rule:
    label: str
    latex_label: str

    def __str__(self):
        return self.label

    def latex(self):
        return self.latex_label


class IntroductionRule(Rule):
    pass


class EliminationRule(Rule):
    pass


class EFQ(Rule):
    label = "EFQ"
    latex_label = "EFQ"

    def __init__(self, intro: SequentItem):
        self.intro = intro

    def apply(self, target: SequentItem, counter=count(1)):
        assert target.sign == sign.POSITIVE, "Invalid application"
        # TODO: Fix this
        assert str(target.fml) == "⊥", "Not an atom"

        target.subproof.derived_by = self

        item = SequentItem(
            self.intro.fml,
            sign=sign.POSITIVE,
            n=next(counter),
        )
        sq, _target = _apply(target, [item], counter)

        # Subproof
        item.subproof = NDSubproof(
            item,
            parent=target.sequent.right[0].subproof,
            children=[target.subproof],
        )
        # target.subproof = Node(target, children=[item.subproof])
        # _target.sequent.right[0].subproof = target.sequent.right[0].subproof
        sq.right[0].subproof = target.sequent.right[0].subproof

        if sq.tautology():
            target.sequent.right[0].subproof.children = item.subproof.children

        return {
            "queue_items": [sq],
            "counter": counter,
        }


class Negation:
    # Intro = signed_rules.NegativeNegationRule
    class Intro(IntroductionRule):
        label = "¬I"
        latex_label = r"$\neg$I"

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Cannot apply introduction rule"
            assert isinstance(target.fml, forms.Negation), "Not a negation"
            subfml = target.fml.sub

            if target.sequent:
                target.subproof.derived_by = self

            # TODO: Fix this
            falsum = forms.Atom("⊥")

            antec = SequentItem(subfml, sign=sign.POSITIVE, n=next(counter))
            conseq = SequentItem(
                falsum,
                sign=sign.NEGATIVE,
                n=next(counter),
            )
            sq = _apply(target, [antec, conseq], counter, preserve_target=False)

            # Subproof
            conseq.subproof = NDSubproof(
                conseq,
                children=[deepcopy(node.subproof) for node in target.sequent.left],
            )
            target.sequent.right[0].subproof.children = [conseq.subproof]
            antec.subproof = NDSubproof(
                antec,
                parent=conseq.subproof,
                children=[],
            )

            return {
                "queue_items": [sq],
                "counter": counter,
            }

    class Elim(EliminationRule):
        label = "¬E"
        latex_label = r"$\neg$E"

        def __init__(self):
            pass

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Negation), "Not a negation"

            target.subproof.derived_by = self

            subfml = target.fml.sub

            # TODO: Better way to check conditions
            # premises = list(map(lambda x: str(x.fml), target.sequent.left))
            # assert str(subfml) in premises, f"`{str(subfml)}` must be in premises"
            subfml = next(
                filter(lambda x: str(x.fml) == str(subfml), target.sequent.left),
                None,
            )
            assert subfml, f"`{str(subfml)}` must be in premises"

            falsum = forms.Atom("⊥")
            item = SequentItem(falsum, sign=sign.POSITIVE, n=next(counter))
            sequent, target = _apply(target, [item], counter)

            # Subproof
            item.subproof = NDSubproof(
                item,
                children=[
                    deepcopy(subfml.subproof),
                    deepcopy(target.subproof),
                ],
                parent=target.sequent.right[0].subproof,
            )
            sequent.right[0].subproof = target.sequent.right[0].subproof

            return {
                "queue_items": [sequent],
                "counter": counter,
            }


class Conjunction:
    # Intro = signed_rules.NegativeConjunctionRule
    # class Intro(signed_rules.NegativeConjunctionRule, IntroductionRule):
    #     pass

    class Intro(IntroductionRule):
        label = "∧I"
        latex_label = r"$\land$I"

        def __init__(self):
            pass

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Cannot apply introduction rule"
            assert isinstance(target.fml, forms.Conjunction), "Not a conjunction"

            target.subproof.derived_by = self

            branches = []

            for conj in target.fml.subs:
                conj = SequentItem(conj, sign=sign.NEGATIVE, n=next(counter))
                sequent = _apply(target, [conj], counter, preserve_target=False)
                branches.append(sequent)

            # Subproof
            for branch in branches:
                for item in branch.left:
                    if getattr(item, "subproof", None) is None:
                        item.subproof = NDSubproof(item)

                branch.right[0].subproof = NDSubproof(branch.right[0])
                branch.right[0].subproof.children = [
                    deepcopy(item.subproof) for item in branch.left
                ]

                if branch.tautology():
                    left_item = next(
                        filter(
                            lambda x: str(x.fml) == str(branch.right[0]), branch.left
                        ),
                        None,
                    )
                    branch.right[0].subproof.children = left_item.subproof.children

            target.sequent.right[0].subproof.children = [
                branch.right[0].subproof for branch in branches
            ]

            return {
                "queue_items": branches,
                "counter": counter,
            }

    # TODO: Choice of conjunct
    # Elim = signed_rules.PositiveConjunctionRule
    class Elim(EliminationRule):
        label = "∧E"
        latex_label = r"$\land$E"

        def __init__(self, conjunct: Literal["left", "right"]):
            self.conjunct = conjunct

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Conjunction), "Not a conjunction"

            target.subproof.derived_by = self

            conj1, conj2 = target.fml.subs
            if self.conjunct == "left":
                item = SequentItem(conj1, sign=sign.POSITIVE, n=next(counter))
            elif self.conjunct == "right":
                item = SequentItem(conj2, sign=sign.POSITIVE, n=next(counter))

            sq1, target = _apply(target, [item], counter)
            # sq2 = Sequent([target], [item], parent=target.sequent)

            # Subproof
            item.subproof = NDSubproof(
                item,
                children=[target.subproof],
                parent=target.sequent.right[0].subproof,
            )

            return {
                "queue_items": [sq1],
                "counter": counter,
            }


class Disjunction:
    # Intro = signed_rules.NegativeDisjunctionRule
    class Intro(IntroductionRule):
        label = "∨I"
        latex_label = r"$\lor$I"

        def __init__(self, disjunct: Literal["left", "right"]):
            self.disjunct = disjunct

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Sign is not negative"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"

            target.subproof.derived_by = self

            disj1, disj2 = target.fml.subs

            if self.disjunct == "left":
                item = SequentItem(disj1, sign=sign.NEGATIVE, n=next(counter))
            elif self.disjunct == "right":
                item = SequentItem(disj2, sign=sign.NEGATIVE, n=next(counter))

            sq = _apply(target, [item], counter, preserve_target=False)

            # Subproof
            item.subproof = NDSubproof(
                item,
                children=[deepcopy(item.subproof) for item in sq.left],
            )
            target.subproof.children = [item.subproof]
            # sq.right[0].subproof = target.sequent.right[0].subproof

            if sq.tautology():
                left_item = next(
                    filter(lambda x: str(x.fml) == str(item.fml), sq.left),
                    None,
                )
                target.subproof.children = [left_item.subproof]

            return {
                "queue_items": [sq],
                "counter": counter,
            }

    # Elim = signed_rules.PositiveDisjunctionRule
    class Elim(EliminationRule):
        label = "∨E"
        latex_label = r"$\lor$E"

        def __init__(self):
            pass

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"

            target.subproof.derived_by = self

            branches = []

            for disj in target.fml.subs:
                disj = SequentItem(disj, sign=sign.POSITIVE, n=next(counter))
                sequent, target = _apply(target, [disj], counter)
                branches.append(sequent)

            # Subproof
            for branch in branches:
                for item in branch.left:
                    if getattr(item, "subproof", None) is None:
                        item.subproof = NDSubproof(item)

                branch.right[0].subproof = NDSubproof(branch.right[0])
                branch.right[0].subproof.children = [
                    deepcopy(item.subproof) for item in branch.left
                ]

            target.sequent.right[0].subproof.children = [
                branch.right[0].subproof for branch in branches
            ] + [target.subproof]

            return {
                "queue_items": branches,
                "counter": counter,
            }


class Conditional:
    # class Intro(signed_rules.NegativeConditionalRule, IntroductionRule):
    #     pass
    class Intro(IntroductionRule):
        label = "→I"
        latex_label = r"$\to$I"

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Cannot apply introduction rule"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"

            target.subproof.derived_by = self

            antec, conseq = target.fml.subs

            antec = SequentItem(antec, sign=sign.POSITIVE, n=next(counter))
            conseq = SequentItem(
                conseq,
                sign=sign.NEGATIVE,
                n=next(counter),
            )
            sq = _apply(target, [antec, conseq], counter, preserve_target=False)

            # Subproof
            conseq.subproof = NDSubproof(
                conseq,
                children=[deepcopy(node.subproof) for node in target.sequent.left],
            )
            target.sequent.right[0].subproof.children = [conseq.subproof]
            antec.subproof = NDSubproof(
                antec,
                parent=conseq.subproof,
                children=[],
            )

            return {
                "queue_items": [sq],
                "counter": counter,
            }

    class Elim(EliminationRule):
        label = "→E"
        latex_label = r"$\to$E"

        def __init__(self):
            pass

        def apply(self, target: SequentItem, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"

            target.subproof.derived_by = self

            antec, conseq = target.fml.subs

            # TODO: Better way to check conditions
            antec = next(
                filter(lambda x: str(x.fml) == str(antec), target.sequent.left),
                None,
            )
            assert antec, "Antecendent does not match"

            # conclusion = str(target.sequent.right[0].fml)
            # print(conclusion)
            # assert str(conseq) == conclusion, "Consequent does not match"

            conseq = SequentItem(conseq, sign=sign.POSITIVE, n=next(counter))
            sequent, _target = _apply(target, [conseq], counter)

            # Subproof
            conseq.subproof = NDSubproof(
                conseq,
                children=[
                    deepcopy(antec.subproof),
                    deepcopy(target.subproof),
                ],
                parent=target.sequent.right[0].subproof,
            )
            # target.sequent.right[0].subproof = sequent.right[0].subproof
            sequent.right[0].subproof = target.sequent.right[0].subproof

            if sequent.tautology():
                target.sequent.right[0].subproof.children = conseq.subproof.children

            return {
                "queue_items": [sequent],
                "counter": counter,
            }
