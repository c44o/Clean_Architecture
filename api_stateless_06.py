import pure_robot

def activate_cleaner(transfer, code, state):
    new_state = pure_robot.make(transfer, code, state)
    return new_state
