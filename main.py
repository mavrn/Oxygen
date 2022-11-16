import sys

from interface import Interface


def main():
    args = sys.argv[1:]
    if len(args) > 0 and args[0].endswith(".oxy"):
        runfile = True
        filepath = args[0]
        args = args[1:]
    else:
        runfile = False
    
    interface_args = {"debug": False, "fallthrough": False, "printall": False, "autoid" : False}
    for arg in args:
        if arg in interface_args:
            interface_args[arg] = True
    interface = Interface(debug=interface_args["debug"],
                          quit_after_exceptions=interface_args["fallthrough"],
                          printall=interface_args["printall"],
                          autoid = interface_args["autoid"])
    if runfile:
        interface.run_from_file(filepath)
    else:
        interface.start_session()


if __name__ == '__main__':
    main()
