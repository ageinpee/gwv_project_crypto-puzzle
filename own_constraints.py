# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:29:44 2018

@author: twiefel
"""
from constraint import Constraint
from constraint import Unassigned
class AddConstraint(Constraint):
    """
    Constraint enforcing that values of given variables sum at least
    to a given amount
    Example:
    >>> problem = Problem()
    >>> problem.addVariables(["a", "b"], [1, 2])
    >>> problem.addConstraint(MinSumConstraint(3))
    >>> sorted(sorted(x.items()) for x in problem.getSolutions())
    [[('a', 1), ('b', 2)], [('a', 2), ('b', 1)], [('a', 2), ('b', 2)]]
    """

    def __init__(self, variables):
        """
        @param minsum: Value to be considered as the minimum sum
        @type  minsum: number
        @param multipliers: If given, variable values will be multiplied by
                            the given factors before being summed to be checked
        @type  multipliers: sequence of numbers
        """
        self.variables = variables

    def __call__(self, variables, domains, assignments, forwardcheck=False):
        print(variables)
        print(domains)
        print(assignments)
        raw_input()
        res = variables[-1]
        uebertrag = variables[-2]
        if res+uebertrag==variables[0]+variables[1]+variables[2]+variables[3]+variables[4]:
            return True
        return False
        
class OurAllDifferentConstraint(Constraint):
    """
    Constraint enforcing that values of all given variables are different
    Example:
    >>> problem = Problem()
    >>> problem.addVariables(["a", "b"], [1, 2])
    >>> problem.addConstraint(AllDifferentConstraint())
    >>> sorted(sorted(x.items()) for x in problem.getSolutions())
    [[('a', 1), ('b', 2)], [('a', 2), ('b', 1)]]
    """
    def __init__(self, variables):
        self.variables = variables
        
        
    def __call__(self, variables, domains, assignments, forwardcheck=False, _unassigned=Unassigned):
        seen = {}
        for variable in variables:
            if variable in self.variables:
                value = assignments.get(variable, _unassigned)
                if value is not _unassigned:
                    if value in seen:
                        return False
                    seen[value] = True
        if forwardcheck:
            for variable in variables:
                if variable in self.variables:
                    if variable not in assignments:
                        domain = domains[variable]
                        for value in seen:
                            if value in domain:
                                domain.hideValue(value)
                                if not domain:
                                    return False
        return True