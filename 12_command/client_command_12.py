import pure_robot
from command_robot_12 import MoveCommand, TurnCommand, SetCommand, StartCommand, StopCommand, CommandExecutor

def main():
    commands = [
        MoveCommand(100),
        TurnCommand(-90),
        SetCommand("soap"),
        StartCommand(),
        MoveCommand(50),
        StopCommand(),
    ]

    executor = CommandExecutor()
    final_state = executor.execute_all(commands)

    print("program finished")
    print("final state: ", final_state)


if __name__ == "__main__":
    main()
