from skfuzzy import control as ctrl
from .fuzzification_module import define_fuzzy_variables
from .fuzzy_rule_base import define_fuzzy_rules

def create_fuzzy_controller(context='waiting_time'):
    """
    Create a fuzzy controller based on defined variables and rules for a specific context.

    Args:
        context (str): Specify whether the controller is for 'waiting_time' or 'walking_speed'.
    
    Returns:
        ControlSystemSimulation: A fuzzy control system simulation object.
    """
    # Define variables based on context
    variables = define_fuzzy_variables(context=context)

    # Define fuzzy rules based on context
    rules = define_fuzzy_rules(variables, context=context)

    # Create the control system
    control_system = ctrl.ControlSystem(rules)

    # Create a control system simulation object
    return ctrl.ControlSystemSimulation(control_system)