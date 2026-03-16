from concatenative_robot_10 import RobotServer

def main():
    server = RobotServer()

    test_workflow = "100 move -90 turn soap set start 50 move stop"
    rest_of_stack = server.execute(test_workflow)

    print("программа завершена")

if __name__ == "__main__":
    main()
