from robot_impl import *

robot0 = Robot.create()
print(robot0)
move_result = robot0.move(100)
robot1 = move_result.robot
print(move_result)
print(robot1)

robot2 = robot1.turn(-90)
print(robot2)

mode_result = robot2.set_mode(CleaningMode.SOAP)
robot3 = mode_result.robot
print(mode_result)
print(robot3)

robot4 = robot3.move(50).robot
print(robot4)
print("Исходный robot0 не остался как был", robot0)
