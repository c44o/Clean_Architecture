from ast_robot_16 import (
    Move,
    Turn,
    SetState,
    Start,
    Stop,
    RobotInterpreter,
)


def build_program():
    return Move(
        100,
        lambda move_resp: Turn(
            -90 if move_resp.ok else 0,
            lambda turn_resp: SetState(
                "soap",
                lambda state_resp:
                    Start(
                        lambda start_resp: Move(
                            50,
                            lambda move_resp_2: Stop()
                        )
                    )
                    if state_resp.ok
                    else Stop()
            )
        )
    )


def main():
    program = build_program()
    interpreter = RobotInterpreter()

    final_state, messages = interpreter.run(program)

    print("final_state =", final_state)
    print("messages =", messages)


if __name__ == "__main__":
    main()
