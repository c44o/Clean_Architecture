import pure_robot
from func_dependency_injection_08 import run_program

def transfer(message):
    print(message)

testing_robot_path_program = (
    "move 100",
    "turn -90",
    "set soap",
    "start", 
    "move 50",
    "stop"
)

initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

resulting_state = run_program(
    transfer, 
    testing_robot_path_program, 
    initial_state,
    move_functional=pure_robot.move,
    turn_functional=pure_robot.turn,
    set_functional=pure_robot.set_state,
    start_functional=pure_robot.start,
    stop_functional=pure_robot.stop,
)

print(resulting_state.x, resulting_state.y, resulting_state.angle, resulting_state.state)
