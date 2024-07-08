from __future__ import annotations

from itertools import count

from anytree import NodeMixin, PostOrderIter, RenderTree

from mathesis.deduction import natural_deduction
from mathesis.deduction.sequent_calculus import SequentTree
from mathesis.deduction.sequent_calculus.sequent import SequentItem
from mathesis.forms import Formula


class NDSubproof(NodeMixin):
    derived_by: natural_deduction.rules.Rule | None

    def __init__(self, item: SequentItem, *, parent=None, children=[]) -> None:
        super().__init__()
        self.name = item
        self.item = item
        self.parent = parent
        self.children = children

        self.derived_by = None


class NDTree:
    """A natural deduction proof tree."""

    _sequent_tree: SequentTree
    bookkeeper: dict[int, SequentItem]
    counter: count[int]

    def __init__(self, premises: list[Formula], conclusion: Formula):
        assert isinstance(conclusion, Formula), "Conclusion must be a single formula"
        self._sequent_tree = SequentTree(premises, [conclusion])
        self.bookkeeper = self._sequent_tree.bookkeeper
        self.counter = self._sequent_tree.counter

        # Proof tree
        for item in self._sequent_tree.root.left:
            item.subproof = NDSubproof(item, children=[])
        self._sequent_tree.root.right[0].subproof = NDSubproof(
            self._sequent_tree.root.right[0],
            children=[item.subproof for item in self._sequent_tree.root.left],
        )

    def __getitem__(self, index):
        return self.bookkeeper[index]

    def apply(self, target: SequentItem, rule):
        res = rule.apply(target, self.counter)
        queue_items = res["queue_items"]

        # new_sequents = []

        for branch in queue_items:
            for node in branch.items:
                self.bookkeeper[node.n] = node
            branch.parent = target.sequent
            # new_sequents.append(branch)

        return self

    def tree(self, style=None, number=True):
        if style == "gentzen":
            output = ""
            root = self._sequent_tree.root.right[0].subproof
            for pre, fill, node in RenderTree(root):
                output += "{}{}{}\n".format(
                    pre,
                    f"[{node.name}]" if getattr(node, "marked", False) else node.name,
                    # self.proof_tree.mapping[node].n,
                    " ×" if getattr(node, "marked", False) else "",

                )
            return output
        else:
            return self._sequent_tree.tree(number=number)

    def latex(self, number=False, arrow=r"\Rightarrow"):
        output = ""
        root = self._sequent_tree.root.right[0].subproof
        for node in PostOrderIter(root):
            if node.derived_by is not None and hasattr(node.derived_by, "latex"):
                label_part = f"\\RightLabel{{{node.derived_by.latex()}}}\n"
            else:
                label_part = ""

            tmpl = ""
            if len(node.children) == 0:
                tmpl = r"\AxiomC{{${}$}}"
            elif len(node.children) == 1:
                tmpl = r"\UnaryInfC{{${}$}}"
            elif len(node.children) == 2:
                tmpl = r"\BinaryInfC{{${}$}}"
            elif len(node.children) == 3:
                tmpl = r"\TrinaryInfC{{${}$}}"
            output += label_part + tmpl.format(node.name.fml.latex()) + "\n"

        return """\\begin{{prooftree}}\n{}\\end{{prooftree}}""".format(output)
