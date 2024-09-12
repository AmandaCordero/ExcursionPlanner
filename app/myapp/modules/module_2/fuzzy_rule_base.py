from skfuzzy import control as ctrl

def define_fuzzy_rules(variables, context='waiting_time'):
    """
    Define the fuzzy rules for the fuzzy inference system.

    Args:
        variables (dict): Dictionary containing all fuzzy variables.
        context (str): Specify whether to define rules for 'waiting_time' or 'walking_speed'.
    
    Returns:
        list: A list of fuzzy rules.
    """
    rules = []

    if context == 'waiting_time':
        # Rules for waiting time
        rules.append(ctrl.Rule(variables['user_history']['low'], variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_history']['medium'] & variables['point_history']['low'], 
                               variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_history']['medium'] & (variables['point_history']['medium'] | variables['point_history']['high']), 
                               variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_history']['high'] & variables['point_history']['low'], 
                               variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_history']['high'] & variables['point_history']['medium'], 
                               variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_history']['high'] & variables['point_history']['high'], 
                               variables['waiting_time']['long']))
        
        # Rules for rivers interest
        rules.append(ctrl.Rule(variables['user_rivers']['low'], variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_rivers']['medium'] & variables['point_rivers']['low'], 
                            variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_rivers']['medium'] & (variables['point_rivers']['medium'] | variables['point_rivers']['high']), 
                            variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_rivers']['high'] & variables['point_rivers']['low'], 
                            variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_rivers']['high'] & variables['point_rivers']['medium'], 
                            variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_rivers']['high'] & variables['point_rivers']['high'], 
                            variables['waiting_time']['long']))

        # Rules for flora interest
        rules.append(ctrl.Rule(variables['user_flora']['low'], variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_flora']['medium'] & variables['point_flora']['low'], 
                            variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_flora']['medium'] & (variables['point_flora']['medium'] | variables['point_flora']['high']), 
                            variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_flora']['high'] & variables['point_flora']['low'], 
                            variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_flora']['high'] & variables['point_flora']['medium'], 
                            variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_flora']['high'] & variables['point_flora']['high'], 
                            variables['waiting_time']['long']))

        # Rules for fauna interest
        rules.append(ctrl.Rule(variables['user_fauna']['low'], variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_fauna']['medium'] & variables['point_fauna']['low'], 
                            variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_fauna']['medium'] & (variables['point_fauna']['medium'] | variables['point_fauna']['high']), 
                            variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_fauna']['high'] & variables['point_fauna']['low'], 
                            variables['waiting_time']['short']))
        rules.append(ctrl.Rule(variables['user_fauna']['high'] & variables['point_fauna']['medium'], 
                            variables['waiting_time']['medium']))
        rules.append(ctrl.Rule(variables['user_fauna']['high'] & variables['point_fauna']['high'], 
                            variables['waiting_time']['long']))


    elif context == 'walking_speed':
        # Fauna interest and path fauna rules
        rules.append(ctrl.Rule(variables['user_fauna']['low'], variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_fauna']['medium'] & variables['path_fauna']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_fauna']['medium'] & (variables['path_fauna']['medium'] | variables['path_fauna']['high']), 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_fauna']['high'] & variables['path_fauna']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_fauna']['high'] & variables['path_fauna']['medium'], 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_fauna']['high'] & variables['path_fauna']['high'], 
                            variables['walking_speed']['fast']))

        # Flora interest and path flora rules
        rules.append(ctrl.Rule(variables['user_flora']['low'], variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_flora']['medium'] & variables['path_flora']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_flora']['medium'] & (variables['path_flora']['medium'] | variables['path_flora']['high']), 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_flora']['high'] & variables['path_flora']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_flora']['high'] & variables['path_flora']['medium'], 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_flora']['high'] & variables['path_flora']['high'], 
                            variables['walking_speed']['fast']))

        # Isolation interest and path isolation rules
        rules.append(ctrl.Rule(variables['user_isolation']['low'], variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_isolation']['medium'] & variables['path_isolation']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_isolation']['medium'] & (variables['path_isolation']['medium'] | variables['path_isolation']['high']), 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_isolation']['high'] & variables['path_isolation']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_isolation']['high'] & variables['path_isolation']['medium'], 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_isolation']['high'] & variables['path_isolation']['high'], 
                            variables['walking_speed']['fast']))

        # Physical challenge interest and path challenge rules
        rules.append(ctrl.Rule(variables['user_challenge']['low'], variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_challenge']['medium'] & variables['path_challenge']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_challenge']['medium'] & (variables['path_challenge']['medium'] | variables['path_challenge']['high']), 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_challenge']['high'] & variables['path_challenge']['low'], 
                            variables['walking_speed']['slow']))
        rules.append(ctrl.Rule(variables['user_challenge']['high'] & variables['path_challenge']['medium'], 
                            variables['walking_speed']['moderate']))
        rules.append(ctrl.Rule(variables['user_challenge']['high'] & variables['path_challenge']['high'], 
                            variables['walking_speed']['fast']))


    return rules
    