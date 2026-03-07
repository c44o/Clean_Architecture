from pure_robot_engine_07 import PureRobotEngine
from cleaner_api import CleanerApi

api = CleanerApi(PureRobotEngine())
api.activate_cleaner(("move 100", "turn -90", "set soap", "start", "move 50", "stop"))
