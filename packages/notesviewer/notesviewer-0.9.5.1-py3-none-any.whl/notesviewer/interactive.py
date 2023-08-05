""" interactive module """

import readline
import notesviewer.vardata
import notesviewer.commands


def checkinput(text):
    """ check input """

    for index in notesviewer.vardata.COMMAND_MODE:
        if text == index:
            return True
    return False


def interactive():
    """ interactive main command """

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    prompt = ""
    while prompt != 'quit':
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
        prompt = input(">>> ")
        if checkinput(prompt) is False:
            print("Unknown Command")
        else:
            process_interactive_command(prompt)


def process_interactive_command(user_input):
    """ process interactive command """

    if user_input == "version":
        notesviewer.commands.cm_version()
    if user_input == "settings":
        print("Choose your settings..")
        notesviewer.interactive.cm_setcommand_mode(1)
    if user_input == "scope":
        notesviewer.interactive.cm_setcommand_mode(2)
    if user_input == "exit":
        if notesviewer.vardata.COMMAND_MODE == "commands_settings":
            notesviewer.interactive.cm_setcommand_mode(1)


def completer(text, state):
    """ custome completer function for readline autocompletion"""
    cmnds = [x for x in notesviewer.vardata.COMMAND_MODE
             if x.startswith(text)]

    try:
        return cmnds[state]

    except IndexError:
        return None


def cm_setcommand_mode(mode):
    """ set command to point to list index """

    if mode == 0:
        notesviewer.vardata.set_command_mode(
            notesviewer.vardata.INTERACTIVE_COMMANDS[0])
    if mode == 1:
        notesviewer.vardata.set_command_mode(
            notesviewer.vardata.INTERACTIVE_COMMANDS[1])
    if mode == 2:
        notesviewer.vardata.set_command_mode(
            notesviewer.vardata.INTERACTIVE_COMMANDS[2])


def get_mode():
    """ return COMMAND_MODE list index """

    count = 0
    for i in notesviewer.vardata.INTERACTIVE_COMMANDS:
        if i == notesviewer.vardata.COMMAND_MODE:
            return count
        count = count + 1

    return False
