from event_sourcing_robot_13 import (
    InMemoryEventStore,
    CommandHandler,
    MoveCommand,
    TurnCommand,
    SetModeCommand,
    StartCleaningCommand,
    StopCleaningCommand,
    rebuild_state,
    build_log,
)

def main():
    robot_id = "robot_1"
    store = InMemoryEventStore()
    handler = CommandHandler(store)

    handler.handle(MoveCommand(robot_id, 100))
    handler.handle(TurnCommand(robot_id, -90))
    handler.handle(SetModeCommand(robot_id, "soap"))
    handler.handle(StartCleaningCommand(robot_id))
    handler.handle(MoveCommand(robot_id, 50))
    handler.handle(StopCleaningCommand(robot_id))

    all_robot_events = store.load_for_robot(robot_id)
    final_state = rebuild_state(all_robot_events)
    log_lines = build_log(all_robot_events)

    print("Final state:", final_state)
    print("Event log:", log_lines)

    partial_state = rebuild_state(all_robot_events[:3])
    print("State after first 3 events:", partial_state)


if __name__ == "__main__":
    main()
