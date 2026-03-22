import pure_robot

class Command:
    def execute(self, transfer, state):
        raise NotImplementedError("в интерфесе метод обозначен, а не реализован")
    

class MoveCommand(Command):
    def __init__(self, distance):
        self.distance = distance

    def execute(self, transfer, state):
        return pure_robot.move(transfer, self.distance, state)
    

class TurnCommand(Command):
    def __init__(self, angle):
        self.angle = angle

    def execute(self, transfer, state):
        return pure_robot.turn(transfer, self.angle, state)
    

class SetCommand(Command):
    def __init__(self, mode):
        self.mode = mode

    def execute(self, transfer, state):
        return pure_robot.set_state(transfer, self.mode, state)

class StartCommand(Command):
    def execute(self, transfer, state):
        return pure_robot.start(transfer, state)
    

class StopCommand(Command):
    def execute(self, transfer, state):
        return pure_robot.stop(transfer, state)
    
class CommandExecutor:
    def __init__(self, transfer=None, initial_state=None):
        if transfer is None:
            transfer = pure_robot.transfer_to_cleaner

        if initial_state is None:
            initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        self.transfer = transfer 
        self.initial_state = initial_state

    def execute_all(self, commands):
        state = self.initial_state

        for command in commands:
            state = command.execute(self.transfer, state)

        return state
    
