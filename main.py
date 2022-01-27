import interface
import sys


def main():
    args = sys.argv[1:]
    interface_args = {"debug": False, "quit_after_exceptions": False}
    for arg in args:
        if arg in interface_args:
            interface_args[arg] = True

    interface.start_session(debug=interface_args["debug"],
                            quit_after_exceptions=interface_args["quit_after_exceptions"])


if __name__ == '__main__':
    main()
