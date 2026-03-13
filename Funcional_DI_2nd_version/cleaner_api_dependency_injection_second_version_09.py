import pure_robot

def apply_pure(transfer, state, command: str):
    cmd = command.split(' ')
    option = cmd[0]

    if option == 'move':
        return pure_robot.move(transfer, int(cmd[1]), state)
    if option == 'turn':
        return pure_robot.turn(transfer, int(cmd[1]), state)
    if option == 'set':
        return pure_robot.set_state(transfer, cmd[1], state)
    if option == 'start':
        return pure_robot.start(transfer, state)
    if option == 'stop':
        return pure_robot.stop(transfer, state)
    
    raise ValueError(f"{command} - какая-то неизвестная команда")


class RobotApi:
    # одна f_apply вместо пяти разных функций из 
    # def setup(self, f_move,f_turn,f_set_state,f_start,f_stop, f_transfer):
    # а диспатч команд теперь в отдельной apply_pure
    def setup(self, f_apply, f_transfer):
        self.f_apply = f_apply
        self.f_transfer = f_transfer

    def make(self, command: str):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        self.cleaner_state = self.f_apply(self.f_transfer, self.cleaner_state, command)
        return self.cleaner_state
    
    # оборачиваем make в __call__, чтобы класс стал вызываемым - для api('move 100') и остальных
    def __call__(self, command:str):
        return self.make(command)
    

def apply_double_move(transfer, state, command:str):
    cmd = command.split(' ')
    if cmd[0] == 'move':
        return pure_robot.move(transfer, int(cmd[1]) * 2, state)
    return apply_pure(transfer, state, command)


def transfer_to_cleaner(message):
    print(message)

api = RobotApi()
# собстенно, инъекция обеих зависимостей
api.setup(apply_pure, transfer_to_cleaner)

