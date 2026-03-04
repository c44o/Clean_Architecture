import pure_robot
from api_stateless_06 import activate_cleaner

def transfer(message):
    print(message)

state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

program_to_run = (
    "move 100",
    "turn -90",
    "set soap", 
    "start", 
    "move 50", 
    "stop"
)

state = activate_cleaner(transfer, program_to_run, state)
