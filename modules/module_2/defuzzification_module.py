from .fuzzy_interface_engine import create_fuzzy_controller

def compute_fuzzy_output(context='waiting_time', **inputs):
    """
    Compute the fuzzy output (either waiting time or walking speed) using the fuzzy control system.

    Args:
        context (str): The context for the fuzzy system, either 'waiting_time' or 'walking_speed'.
        inputs (dict): Dictionary of input values for the fuzzy system.
    
    Returns:
        float: The computed fuzzy output (waiting time or walking speed).
    """
    # Initialize fuzzy controller
    simulation = create_fuzzy_controller(context=context)

    # Pass inputs to the fuzzy controller
    for key, value in inputs.items():
        simulation.input[key] = value

    # Compute the output
    simulation.compute()

    return simulation.output[context]
