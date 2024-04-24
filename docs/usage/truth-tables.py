# %% [markdown]
# # Truth tables

# ## Show truth tables for connectives

# Truth functions are defined as _clauses_ in mathesis.
# You can show the truth tables for the clauses in HTML in JupyerLab/Jupyter Notebook:

# %%
from mathesis.system.classical.truth_table import ConditionalClause

conditional_clause = ConditionalClause()
conditional_clause

# %% [markdown]
# Outside Jupyer, you get a plain text table:
# %%
print(conditional_clause)

# %% [markdown]
# ## Generate truth tables for classical logic

# `mathesis.semantics.truth_table.ClassicalTruthTable` automatically generates the truth table for a given formula.

# %%
from mathesis.grammars import BasicGrammar
from mathesis.semantics.truth_table import ClassicalTruthTable

grammar = BasicGrammar()

fml = grammar.parse("(¬P∧(P∨Q))→Q")

table = ClassicalTruthTable(fml)
table

# %% [markdown]
# `table.is_valid()` just returns whether the formula is valid.

# %%
f"Valid: {table.is_valid()}"

# %% [markdown]
# ## Generate truth tables for many-valued logics

# Some many-valued logics are implemented out of the box. They are available from `mathesis.semantics.truth_table`.

# %% [markdown]
# ### Three-valued logic K<sub>3</sub> and Ł<sub>3</sub>

# #### Kleene's K<sub>3</sub>

# %%
from mathesis.grammars import BasicGrammar
from mathesis.semantics.truth_table import K3TruthTable

grammar = BasicGrammar()

fml = grammar.parse("A∨¬A")

table = K3TruthTable(fml)
table

# %%
f"Valid: {table.is_valid()}"

# %% [markdown]
# #### Łukasiewicz's Ł<sub>3</sub>

# WIP

# %% [markdown]
# ### Three-valued logic LP

# %%
from mathesis.grammars import BasicGrammar
from mathesis.semantics.truth_table import LPTruthTable

grammar = BasicGrammar()

fml = grammar.parse("(A∧¬A)→A")

table = LPTruthTable(fml)
table

# %%
f"Valid: {table.is_valid()}"

# %% [markdown]
# ### Four-valued logic FDE

# WIP

# %% [markdown]
# ## Use custom symbols for truth values

# Subclasses of `ConnectiveClause()` and `TruthTable()` can have `truth_value_symbols` attribute that is a dictionary mapping internal numeric truth values to arbitrary symbols like ⊤, ⊥, T, F, etc.

# %% [markdown]
# ## Define custom truth tables

# WIP
