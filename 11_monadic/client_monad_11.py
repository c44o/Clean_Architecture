import pure_robot
from state_monad_robot_13 import (
    StateMonad,
    move_m,
    turn_m,
    set_state_m,
    start_m,
    stop_m,
)


def main():
    transfer = pure_robot.transfer_to_cleaner

    initial_state = pure_robot.RobotState(
        0.0,
        0.0,
        0,
        pure_robot.WATER
    )

    program = (
        StateMonad.unit(None)
        .then(move_m(transfer, 100))
        .then(turn_m(transfer, -90))
        .then(set_state_m(transfer, "soap"))
        .then(start_m(transfer))
        .then(move_m(transfer, 50))
        .then(stop_m(transfer))
    )

    result, final_state = program.run(initial_state)

    print("программа закончена")
    print("получилось ", result)
    print("итоговое состояние ", final_state)


if __name__ == "__main__":
    main()
