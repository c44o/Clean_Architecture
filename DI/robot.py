import pure_robot

SQUARE_TO_CLEAN_SIZE = 1500
BASIC_ROBOT_STEP = 50

def default_transfer(message):
    print(message)

class Robot:
    def __init__(self, transfer=default_transfer):
        self._transfer = transfer
        self._state = pure_robot.RobotState(0, 0, 0, pure_robot.WATER)

    def _move(self, distance: int):
        self._state = pure_robot.move(self._transfer, distance, self._state)

    def _turn(self, angle: int):
        self._state = pure_robot.turn(self._transfer, angle, self._state)

    def _set(self, mode: str):
        self._state = pure_robot.set_state(self._transfer, mode, self._state)

    def _start(self):
        self._state = pure_robot.start(self._transfer, self._state)

    def _stop(self):
        self._state = pure_robot.stop(self._transfer, self._state)

    def clean_square(self, size: int, step: int):
        render = (1, size // step)
        for i in range(render):
            self._move(size)
            if i == render - 1:
                break
            if i % 2 == 0:
                self._turn(90)
                self._move(step)
                self._move(90)
            if i % 2 != 0:
                self._turn(-90)
                self._move(step)
                self._turn(-90)

    # сам API
    def water_cleaning(self):
        self._set("water")
        self._start()
        self.clean_square(SQUARE_TO_CLEAN_SIZE, BASIC_ROBOT_STEP)
        self._stop()

    def soap_cleaning(self):
        self._set("soap")
        self._start()
        self.clean_square(SQUARE_TO_CLEAN_SIZE, BASIC_ROBOT_STEP)
        self._stop()

    def brush_cleaning(self):
        self._set("brush")
        self._start()
        self.clean_square(SQUARE_TO_CLEAN_SIZE, BASIC_ROBOT_STEP)
        self._stop()
