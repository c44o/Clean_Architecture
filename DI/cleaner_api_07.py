import pure_robot
from engine_protocol_07 import RobotEngine, Transfer

class CleanerApi:
    def __init__(self, engine: RobotEngine[pure_robot.RobotState], transfer: Transfer = print):
        self.engine = engine
        self.transfer = transfer
        self.state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)


    def activate_cleaner(self, code):
        for command in code:
            cmd = command.split(" ")
            if cmd[0] == "move":
                self.state = self.engine.move(self.transfer, int(cmd[1]), self.state)
            elif cmd[0] == "turn":
                self.state = self.engine.turn(self.transfer, int(cmd[1]), self.state)
            elif cmd[0] == "set":
                self.state = self.engine.set_state(self.transfer, cmd[1], self.state)
            elif cmd[0] == "start":
                self.state = self.engine.start(self.transfer, self.state)
            elif cmd[0] == "stop":
                self.state = self.engine.stop(self.transfer, self.state)
