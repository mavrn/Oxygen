from interface import Interface
import sys
import testmodules


def main():
    args = sys.argv[1:]
    interface_args = {"debug": False, "fallthrough": False, "run": False, "printall": False}
    for arg in args:
        if arg in interface_args:
            interface_args[arg] = True
    interface = Interface(debug=interface_args["debug"],
                          quit_after_exceptions=interface_args["fallthrough"])
    if interface_args["run"]:
        interface.run_from_txt(printall=interface_args["printall"])
    else:
        interface.start_session()

if __name__ == '__main__':
    main()