from interface import Interface
import sys
import test_programs


def main():
    args = sys.argv[1:]
    interface_args = {"debug": True, "quit_after_exceptions": True}
    for arg in args:
        if arg in interface_args:
            interface_args[arg] = True
    interface = Interface(debug=interface_args["debug"],
                          quit_after_exceptions=interface_args["quit_after_exceptions"])
    # interface.run(test_programs.test12)
    interface.start_session()


if __name__ == '__main__':
    main()
