import sys

from interface import Interface


def main():
    args = sys.argv[1:]
    if len(args) > 0 and args[0].endswith(".oxy"):
        runfile = True
        filepath = args[0]
        args = args[1:]
        standard_printall = False
    else:
        runfile = False
        standard_printall = True
    
    interface_args = {"debug": False, "fallthrough": False, "printall": standard_printall, "disableautoid": False}
    for arg in args:
        if arg in interface_args:
            interface_args[arg] = not interface_args[arg]
    interface = Interface(debug=interface_args["debug"],
                          quit_after_exceptions=interface_args["fallthrough"],
                          printall=interface_args["printall"],
                          autoid = not interface_args["disableautoid"])
    if runfile:
        interface.run_from_file(filepath)
    else:
        interface.start_session()


if __name__ == '__main__':
    main()
