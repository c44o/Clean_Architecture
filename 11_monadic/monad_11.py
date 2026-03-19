import pure_robot

class StateMonad:
    def __init__(self, run):
        self.run = run

    def bind(self, f):
        def new_run(state):
            value, new_state = self.run(state)
            next_monad = f(value)
            return next_monad.run(new_state)

        return StateMonad(new_run)

    def then(self, next_monad):
        return self.bind(lambda _: next_monad)

    @staticmethod
    def unit(value):
        return StateMonad(lambda state: (value, state))


def move_m(transfer, distance):
    def run(state):
        new_state = pure_robot.move(transfer, int(distance), state)
        return None, new_state

    return StateMonad(run)


def turn_m(transfer, angle):
    def run(state):
        new_state = pure_robot.turn(transfer, int(angle), state)
        return None, new_state

    return StateMonad(run)


def set_state_m(transfer, mode):
    def run(state):
        new_state = pure_robot.set_state(transfer, mode, state)
        return None, new_state

    return StateMonad(run)


def start_m(transfer):
    def run(state):
        new_state = pure_robot.start(transfer, state)
        return None, new_state

    return StateMonad(run)


def stop_m(transfer):
    def run(state):
        new_state = pure_robot.stop(transfer, state)
        return None, new_state

    return StateMonad(run)
