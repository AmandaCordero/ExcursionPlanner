from defuzzification_module import compute_fuzzy_output

if __name__ == "__main__":
    # Example for waiting time
    waiting_time_inputs = {
        'user_history': 0.8,
        'user_rivers': 0.5,
        'user_flora': 0.6,
        'user_fauna': 0.9,
        'point_history': 0.7,
        'point_rivers': 0.2,
        'point_flora': 0.8,
        'point_fauna': 0.9
    }
    waiting_time = compute_fuzzy_output(context='waiting_time', **waiting_time_inputs)
    print(f"Computed waiting time: {round(waiting_time, 2)} minutes")

    # Example for walking speed
    walking_speed_inputs = {
        'user_fauna': 0.7,
        'user_flora': 0.6,
        'user_isolation': 0.8,
        'user_challenge': 0.9,
        'path_fauna': 0.5,
        'path_flora': 0.6,
        'path_isolation': 0.7,
        'path_challenge': 0.8
    }
    walking_speed = compute_fuzzy_output(context='walking_speed', **walking_speed_inputs)
    print(f"Computed walking speed: {walking_speed} km/h")
