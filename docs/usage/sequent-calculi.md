# Proofs using Sequent Calculus

<a href="https://en.wikipedia.org/wiki/Sequent_calculus" target="_blank">Sequent calculus</a> (plural: calculi) is a formal proof system based on *sequents*, which normally are expressions of the form $\Gamma \vdash \Delta$, where $\Gamma$ and $\Delta$ are lists or sets of formulas.

## Sequent trees and applications of rules

`mathesis.deduction.sequent_calculus.SequentTree` is a class for sequent trees (proof trees, proof diagrams).
It is initialized with an inference, given as a list of premises and of conclusions.
Rules are applied to a sequent in a sequent tree with `st.apply(node, rule)` where `st` is a sequent tree.

```python exec="1" result="text" source="above"
from mathesis.deduction.sequent_calculus import SequentTree, rules
from mathesis.grammars import BasicGrammar

grammar = BasicGrammar()
premises = grammar.parse(["¬A", "A∨B"])
conclusions = grammar.parse(["B"])

st = SequentTree(premises, conclusions)

print(st.tree())
st.apply(st[1], rules.Negation.Left())
print(st.tree())
st.apply(st[5], rules.Disjunction.Left())
print(st.tree())
st.apply(st[9], rules.Weakening.Right())
print(st.tree())
st.apply(st[12], rules.Weakening.Right())
print(st.tree())
```

## Render the proof in LaTeX

A sequent tree object can be rendered in LaTeX with `st.latex()`.
The LaTeX output uses a `prooftree` environment of `bussproofs` package.
MathJax supports `bussproofs` package, so you can render the LaTeX output on a Web page.

```python exec="1" result="text" source="above"
from mathesis.deduction.sequent_calculus import SequentTree, rules
from mathesis.grammars import BasicGrammar

grammar = BasicGrammar()
premises = grammar.parse(["¬A", "A∨B"])
conclusions = grammar.parse(["B"])

st = SequentTree(premises, conclusions)

print(st.tree())
print(st.latex(number=False), "\n")

st.apply(st[1], rules.Negation.Left())
# print(st.tree())
st.apply(st[5], rules.Disjunction.Left())
# print(st.tree())
st.apply(st[9], rules.Weakening.Right())
# print(st.tree())
st.apply(st[12], rules.Weakening.Right())
print(st.tree())
print(st.latex(number=False))
```

$$
\begin{prooftree}
\AxiomC{$\neg A, A \lor B \Rightarrow B$}
\end{prooftree}
$$

$$
\begin{prooftree}
\AxiomC{$A \Rightarrow A$}
\UnaryInfC{$A \Rightarrow B, A$}
\AxiomC{$B \Rightarrow B$}
\UnaryInfC{$B \Rightarrow B, A$}
\BinaryInfC{$A \lor B \Rightarrow B, A$}
\UnaryInfC{$\neg A, A \lor B \Rightarrow B$}
\end{prooftree}
$$