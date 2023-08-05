import pytest

import eppy_funcs as ef
from evaluator import EvaluatorEP, EvaluatorSR
from parameters import RangeParameter, CategoryParameter, Parameter, FieldSelector
from problem import EPProblem, Problem
import sampling
import numpy as np


@pytest.fixture
def building():
    #returns the basic building
    return ef.get_building()


@pytest.fixture
def problem():
    parameters = [Parameter(FieldSelector(object_name='Mass NonRes Wall Insulation', field_name='Thickness'))]
    objectives = ['Electricity:Facility', 'Gas:Facility'] # the default is just 'Electricity:Facility'

    problem=EPProblem(parameters, objectives) #EPP Problem automatically converts these to MeterReaders
    return problem


def test_evaluatorEP(building, problem):
    """To make sure EvaluatorEP can be initialised and works as intended"""

    evaluator = EvaluatorEP(problem, building)
    result = evaluator([0.5]) # run with thickness set to 0.5

    assert np.isclose(result[0], 1818735943.9307632) and np.isclose(result[1], 2172045529.871896), f'Unexpected result for EvaluatorEP, {result}'
    #change this to 0 to see stdout and stderr
    assert 1


def test_evaluatorSR(building, problem):
    """To make sure EvaluatorSR can be initialised and works as intended"""
    def function(values):
        return ((values[0], values[0]**2), ())

    # this denotes a problem which takes 1 input, produces 2 outputs and no constraints. The placeholder parameters/objectives will be generated automatically.
    new_problem = Problem(1,2,0)

    evaluator_1 = EvaluatorSR(function, problem)
    evaluator_2 = EvaluatorSR(function, new_problem)
    result_1 = evaluator_1([4])
    result_2 = evaluator_2([4])

    assert result_1 == (4, 16), f'Unexpected result for EvaluatorSR with EPProblem, {result_1}'
    assert result_2 == (4, 16), f'Unexpected result for EvaluatorSR with custom problem, {result_2}'

    #change this to 0 to see stdout and stderr
    assert 1
