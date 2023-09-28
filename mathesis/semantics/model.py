from itertools import permutations
from typing import Any, Callable, Dict, Set

from mathesis import forms
from mathesis.semantics.truth_table import classical as truth_table


def normalize_predicates(predicates):
    return dict(
        map(
            lambda x: (x[0], tuple((v,) for v in x[1]))
            if (len(x[1]) > 0 and type(list(x[1])[0]) is not tuple)
            else x,
            predicates.items(),
        )
    )


class Model:
    def __init__(
        self,
        domain: Set[Any] = set(),
        predicates: Dict[str, Set[Any]] = dict(),
        constants: Dict[str, Any] = dict(),
        variables: Set[str] = set(),
        functions: Dict[str, Callable] = dict(),
    ):
        """
        Args:
            domain (Set): a set of objects
            predicates (Dict): a dictionary with predicate symbols as keys and sets of tuples of objects as values,
                or a function that assigns sets of tuples of objects to predicate symbols
            constants (Dict): a dictionary with constant symbols as keys and objects as values,
                or a function that assigns objects to constants
            variables (Set): a set of variable symbols
            functions (Dict): a dictionary with function symbols as keys and functions over domain as values
        """
        self.domain = domain
        # Make sure that the value of a predicate is a list of tuples
        predicates = normalize_predicates(predicates)
        self.predicates = predicates
        self.constants = constants
        self.variables = variables
        self.functions = functions

        # TODO: Support top and bottom

    def assign_term_denotation(self, term):
        if term in self.variables:
            pass
        elif term in self.constants:
            return self.denotations.get(term, term)

    def valuate(self, fml: forms.Formula, variable_assignment: Dict[str, Any] = dict()):
        """
        Valuates a formula in a model.
        """
        if isinstance(fml, forms.Atom):
            # Denotations of the terms, a list to be converted to a tuple
            term_denotations = []

            # Iterate over all terms in the formula
            for term in fml.terms:
                # print(fml, term)
                if term in self.constants:
                    denotation = self.constants.get(term)

                elif term in self.variables:
                    # If the assignment of the variable is already given, use it
                    if term in variable_assignment:
                        denotation = variable_assignment[term]
                    else:
                        raise RuntimeError(f"Variable assignment not given: '{term}'")

                # Fallback: use the term itself as denotation
                elif term in self.domain:
                    denotation = term

                else:
                    raise NotImplementedError(f"Undefined type of term: '{term}'")

                term_denotations.append(denotation)

            term_denotations = tuple(term_denotations)

            # Obtain the extension of the predicate
            if fml.predicate in self.predicates:
                extension = self.predicates.get(fml.predicate)
            else:
                raise Exception("Undefined predicate")
            # print(term_denotations, extension)

            if term_denotations in extension:
                return "1"
            else:
                return "0"

        elif isinstance(fml, forms.Universal):
            # print(fml.sub, fml.variable, fml.sub.free_terms)
            values = []

            for obj in self.domain:
                # print(fml.variable, obj)
                value = self.valuate(
                    fml.sub,
                    variable_assignment=dict(
                        variable_assignment, **{fml.variable: obj}
                    ),
                )
                values.append(value)

            # Return true if true in all possible assignments
            if all(value == "1" for value in values):
                return "1"
            else:
                return "0"

        elif isinstance(fml, forms.Particular):
            values = []

            for obj in self.domain:
                value = self.valuate(
                    fml.sub,
                    variable_assignment=dict(
                        variable_assignment, **{fml.variable: obj}
                    ),
                )
                values.append(value)

            # Return true if true in some possible assignments
            if any(value == "1" for value in values):
                return "1"
            else:
                return "0"

        elif isinstance(fml, forms.Negation):
            return truth_table.NegationClause().apply(
                self.valuate(fml.sub, variable_assignment=variable_assignment)
            )

        elif isinstance(fml, forms.Conjunction):
            return truth_table.ConjunctionClause().apply(
                *tuple(
                    self.valuate(child, variable_assignment=variable_assignment)
                    for child in fml.subs
                )
            )

        elif isinstance(fml, forms.Disjunction):
            return truth_table.DisjunctionClause().apply(
                *tuple(
                    self.valuate(child, variable_assignment=variable_assignment)
                    for child in fml.subs
                )
            )

        elif isinstance(fml, forms.Conditional):
            return truth_table.ConditionalClause().apply(
                *tuple(
                    self.valuate(child, variable_assignment=variable_assignment)
                    for child in fml.subs
                )
            )

    def validates(self, premises=[], conclusions=[]):
        # List up all free variables in premises and conclusions
        free_variables = set()
        for fml in premises + conclusions:
            free_variables.update(fml.free_terms)
        free_variables -= self.constants.keys()
        # print(free_variables)

        # List up all possible variable assignments
        variable_assignments = []
        for sequence_of_objects in permutations(self.domain, len(free_variables)):
            # print("sequence_of_objects", sequence_of_objects)
            variable_assignment = dict(zip(free_variables, sequence_of_objects))
            variable_assignments.append(variable_assignment)
        # print("variable_assignments", variable_assignments)

        is_valid_with_assignment = []

        for variable_assignment in variable_assignments:
            premise_values = []
            conclusion_values = []

            for fml in premises:
                value = self.valuate(fml, variable_assignment=variable_assignment)
                premise_values.append(value)

            for fml in conclusions:
                value = self.valuate(fml, variable_assignment=variable_assignment)
                conclusion_values.append(value)

            if all(value == "1" for value in premise_values) and any(
                value != "1" for value in conclusion_values
            ):
                is_valid_with_assignment.append(False)
            else:
                is_valid_with_assignment.append(True)

        if all(is_valid_with_assignment):
            return True
        else:
            return False


class KripkeModel:
    pass
