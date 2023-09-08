from operator import itemgetter
from itertools import count
from copy import copy

from anytree import Node, RenderTree, PostOrderIter

from mathesis.deduction.sequent_calculus import Sequent, SequentTree, sign


class Derivation:
    def __init__(self, premises, conclusions):
        self._tableau = SequentTree(premises, conclusions)

    def __getitem__(self, index):
        return self.bookkeeper[index]

    def apply(self, target: Node, rule):
        # print("target", target)
        queue_items = itemgetter("queue_items")(
            rule.apply(target, target, self.counter)
        )
        # print("queue_items", queue_items)
        # # NOTE: check if branched
        for branch in queue_items:
            # print("target_sequent_node", target_sequent_node)
            nodes_in_new_sequent = list(
                filter(
                    lambda x: x.n != target.n and not getattr(x, "weakened", False),
                    list(map(copy, target.sequent_node.sequent[0]))
                    + list(map(copy, target.sequent_node.sequent[1]))
                    + branch,
                )
            )
            left, right = ([], [])
            for node in nodes_in_new_sequent:
                if node.sign == sign.POSITIVE:
                    left.append(node)
                elif node.sign == sign.NEGATIVE:
                    right.append(node)
            for node in nodes_in_new_sequent:
                if node not in branch:
                    node.n = next(self.counter)
                self.bookkeeper[node.n] = node
            sequent = Sequent(left, right)
            sequent_node = Node(
                str(sequent),
                sequent=sequent,
                parent=target.sequent_node,
            )
            for node in nodes_in_new_sequent:
                node.sequent_node = sequent_node
        return self

    def tree(self, number=True):
        output = ""
        for pre, fill, node in RenderTree(self.root):
            output += "{}{}\n".format(
                pre,
                "{} ⇒ {}".format(
                    ", ".join(
                        map(
                            lambda x: x.name + (f" {x.n}" if number else ""),
                            node.sequent[0],
                        )
                    ),
                    ", ".join(
                        map(
                            lambda x: x.name + (f" {x.n}" if number else ""),
                            node.sequent[1],
                        )
                    ),
                ),
            )
        return output

    def latex(self, number=False, arrow=r"\Rightarrow"):
        output = ""
        for node in PostOrderIter(self.root):
            tmpl = ""
            if len(node.children) == 0:
                tmpl = r"\AxiomC{{${}$}}"
            elif len(node.children) == 1:
                tmpl = r"\UnaryInfC{{${}$}}"
            elif len(node.children) == 2:
                tmpl = r"\BinaryInfC{{${}$}}"
            output += tmpl.format(node.sequent.latex()) + "\n"
        return """\\begin{{prooftree}}\n{}\\end{{prooftree}}""".format(output)