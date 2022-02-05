from interface import Interface
import sys
import testing_module


def main():
    args = sys.argv[1:]
    interface_args = {"debug": False, "quit_after_exceptions": False, "run": False, "run_tests": True}
    for arg in args:
        if arg in interface_args:
            interface_args[arg] = True
    interface = Interface(debug=interface_args["debug"],
                          quit_after_exceptions=interface_args["quit_after_exceptions"])
    # interface.run(test_programs.t14)
    if interface_args["run"]:
        interface.run_from_txt()
    elif interface_args["run_tests"]:
        test_programs.test_group.run_tests()
    else:
        interface.start_session()


if __name__ == '__main__':
    main()
