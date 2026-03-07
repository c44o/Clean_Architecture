import pure_robot
from engine_interface_07 import RobotEngine, Transfer

class PureRobotEngine(RobotEngine[pure_robot.RobotState]):
    def move(self, transfer: Transfer, distance: int, state: pure_robot.RobotState):
        return pure_robot.move(transfer, distance, state)
    
    def turn(self, transfer: Transfer, angle: int, state: pure_robot.RobotState):
        return pure_robot.turn(transfer, angle, state)
    
    def set_state(self, transfer: Transfer, mode: str, state: pure_robot.RobotState):
        return pure_robot.set_state(transfer, mode, state)
    
    def start(self, transfer: Transfer, state: pure_robot.RobotState):
        return pure_robot.start(transfer, state)
    
    def stop(self, transfer: Transfer, state: pure_robot.RobotState):
        return pure_robot.stop(transfer, state)
