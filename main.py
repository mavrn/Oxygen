import interface

def main():
    # fractions: Will convert the output into an approximate fraction
    # debug: Will print lexer output and parser output additionally
    # dont_quit_after_exceptions: Will prevent program from quitting after reaching an exception. This is experimental
    # and can lead to unexpected behaviour
    interface.start_session(fractions=False, debug=False, dont_quit_after_exceptions=False)



if __name__ == '__main__':
    main()