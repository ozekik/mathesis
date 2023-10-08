# %% [markdown]
# ## Models
#
# Models can be defined using `Model` class in `mathesis.semantics.model`. The class takes four arguments:
# * `domain`: the domain of objects of the model
# * `constants`: the constant symbols and assigned objects
# * `predicates`: the predicate symbols and extensions
# * `functions` (Optional): the functions symbols and assigned functions

# %%
from mathesis.grammars import BasicGrammar
from mathesis.semantics.model import Model

grammar = BasicGrammar(symbols={"conditional": "→"})

model = Model(
    domain={"a", "b", "c"},
    constants={
        "a": "a",
        "b": "b",
    },
    predicates={
        "P": {"a", "b"},
        "Q": {"a"},
        "R": {("a", "b"), ("c", "a")},
    },
)

# %% [markdown]
# `model.valuate()` takes a formula and a variable assignment and returns the truth value of the formula in the model.

# %%
fml = grammar.parse("P(a) → R(x, b)")
model.valuate(fml, variable_assignment={"x": "c"})

# %%
model.valuate(fml, variable_assignment={"x": "a"})

# %% [markdown]
# `model.validates()` takes premises and conclusions and returns whether the model validates the inference.

# %%
fml = grammar.parse("∀x(∃y((Q(x)∨Q(b))→R(x, y)))")
model.validates(premises=[], conclusions=[fml])

# %% [markdown]
# ## Countermodel construction

# WIP
