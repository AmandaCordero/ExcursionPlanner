import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def define_fuzzy_variables(context='waiting_time'):
    """
    Define fuzzy variables (inputs and outputs) and membership functions.

    Args:
        context (str): Specify whether to define variables for 'waiting_time' or 'walking_speed'.
    
    Returns:
        dict: A dictionary containing the fuzzy variables for user preferences,
              point indices, and the output.
    """
    if context == 'waiting_time':
        # Define fuzzy variables for waiting time
        user_history = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_history')
        user_rivers = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_rivers')
        user_flora = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_flora')
        user_fauna = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_fauna')

        point_history = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'point_history')
        point_rivers = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'point_rivers')
        point_flora = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'point_flora')
        point_fauna = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'point_fauna')

        waiting_time = ctrl.Consequent(np.arange(0, 16, 1), 'waiting_time')

        for var in [user_history, user_rivers, user_flora, user_fauna]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.4])
            var['medium'] = fuzz.trimf(var.universe, [0.3, 0.5, 0.7])
            var['high'] = fuzz.trimf(var.universe, [0.6, 1, 1])

        for var in [point_history, point_rivers, point_flora, point_fauna]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.4])
            var['medium'] = fuzz.trimf(var.universe, [0.3, 0.5, 0.7])
            var['high'] = fuzz.trimf(var.universe, [0.6, 1, 1])

        waiting_time['short'] = fuzz.trimf(waiting_time.universe, [0, 0, 2.5])
        waiting_time['medium'] = fuzz.trimf(waiting_time.universe, [2.5, 5, 7.5])
        waiting_time['long'] = fuzz.trimf(waiting_time.universe, [7.5, 10, 15])

        return {
            'user_history': user_history,
            'user_rivers': user_rivers,
            'user_flora': user_flora,
            'user_fauna': user_fauna,
            'point_history': point_history,
            'point_rivers': point_rivers,
            'point_flora': point_flora,
            'point_fauna': point_fauna,
            'waiting_time': waiting_time
        }

    elif context == 'walking_speed':
        # Define fuzzy variables for walking speed
        user_fauna = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_fauna')
        user_flora = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_flora')
        user_isolation = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_isolation')
        user_challenge = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'user_challenge')

        path_fauna = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'path_fauna')
        path_flora = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'path_flora')
        path_isolation = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'path_isolation')
        path_challenge = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'path_challenge')

        walking_speed = ctrl.Consequent(np.arange(0, 2, 1), 'walking_speed')

        for var in [user_fauna, user_flora, user_isolation, user_challenge]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.4])
            var['medium'] = fuzz.trimf(var.universe, [0.3, 0.5, 0.7])
            var['high'] = fuzz.trimf(var.universe, [0.6, 1, 1])

        for var in [path_fauna, path_flora, path_isolation, path_challenge]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.4])
            var['medium'] = fuzz.trimf(var.universe, [0.3, 0.5, 0.7])
            var['high'] = fuzz.trimf(var.universe, [0.6, 1, 1])

        walking_speed['slow'] = fuzz.trimf(walking_speed.universe, [0, 0, 0.6])
        walking_speed['moderate'] = fuzz.trimf(walking_speed.universe, [0.4, 1, 1.4])
        walking_speed['fast'] = fuzz.trimf(walking_speed.universe, [1.2, 1.6, 2])

        return {
            'user_fauna': user_fauna,
            'user_flora': user_flora,
            'user_isolation': user_isolation,
            'user_challenge': user_challenge,
            'path_fauna': path_fauna,
            'path_flora': path_flora,
            'path_isolation': path_isolation,
            'path_challenge': path_challenge,
            'walking_speed': walking_speed
        }