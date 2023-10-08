# %% [markdown]
#
# Mathesis works well with JupyterLab and Jupyter notebooks. This is an example of a notebook that uses Mathesis.

# %%
from IPython.display import display, Math
# %%
from mathesis.deduction.sequent_calculus import SequentTree, rules
from mathesis.grammars import BasicGrammar

grammar = BasicGrammar()
premises = grammar.parse(["¬A", "A∨B"])
conclusions = grammar.parse(["B"])

# %%

st = SequentTree(premises, conclusions)

Math(st[1].sequent_node.sequent.latex())

# %%
st.apply(st[1], rules.NegationLeft())
print(st.tree())

# %%
st.apply(st[5], rules.DisjunctionLeft())
print(st.tree())

# %%
st.apply(st[9], rules.WeakeningRight())
print(st.tree())

# %%
st.apply(st[12], rules.WeakeningRight())
print(st.tree())