import pure_robot
from stream_processing_robot_13 import (
    EventStore,
    StateProjector,
    CommandHandler,
    RobotEventProcessor,
    MoveCommand,
    TurnCommand,
    SetModeCommand,
    StartCleaningCommand,
    StopCleaningCommand,
    event_to_text,
)


def main():
    robot_id = "robot_001"

    initial_state = pure_robot.RobotState(
        0.0,
        0.0,
        0,
        pure_robot.WATER
    )

    event_store = EventStore()
    projector = StateProjector(initial_state)

    processor = RobotEventProcessor(event_store, projector)
    event_store.subscribe(processor)

    command_handler = CommandHandler(event_store)

    commands = [
        MoveCommand(robot_id, 100),
        TurnCommand(robot_id, -90),
        SetModeCommand(robot_id, "soap"),
        StartCleaningCommand(robot_id),
        MoveCommand(robot_id, 50),
        StopCleaningCommand(robot_id),
    ]

    for command in commands:
        command_handler.handle_command(command)

    events = event_store.get_events(robot_id)
    final_state = projector.project_state(events)

    print("=== Events ===")
    for index, event in enumerate(events, start=1):
        print(index, event_to_text(event))

    print()
    print("Final state:", final_state)


if __name__ == "__main__":
    main()
