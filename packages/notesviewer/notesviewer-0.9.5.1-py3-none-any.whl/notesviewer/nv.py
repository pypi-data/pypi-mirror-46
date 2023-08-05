#!/usr/bin/env python3

""" nv applicaiton """

import argparse
import notesviewer.vardata
import notesviewer.interactive
import notesviewer.commands
from notesviewer.config import loadconfig, set_data_location, \
    set_profile_path, create_default_profile


def main():
    """ main application function """

    loadconfig()
    set_data_location()
    set_profile_path()
    create_default_profile()
    parse_arguments()


def parse_arguments():
    """ parse all the program arguments """

    # create the root parser
    parser = argparse.ArgumentParser(
        prog=notesviewer.vardata.PROGRAM_NAME,
        description="Commandline notes viewer",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # create subparser
    subparser = parser.add_subparsers(dest='cmd')

    # version command
    version_parser = subparser.add_parser(
        'version', help='Show version number'
    )

    # init notes directory
    init_parser = subparser.add_parser(
        'init', help='Initalize note root directory'
    )

    #  add_profile
    add_profile_parser = subparser.add_parser(
        'add_profile', help='Add a new profile'
    )
    add_profile_parser.add_argument(
        'profile', action='store', help='Profile')

    # show profles
    show_parser = subparser.add_parser('show_profiles', help='Show profiles')

    # switch profie
    switch_profile_parser = subparser.add_parser(
        'switch_profile', help='Switch to a profile'
    )
    switch_profile_parser.add_argument(
        'profile', action='store', help='profile'
    )

    # profile
    profile_parser = subparser.add_parser(
        'profile', help='Show current profile'
    )

    # add
    add_parser = subparser.add_parser('add', help='Add a note')
    add_parser.add_argument('note', action='store', help='Note')

    # insert
    add_parser = subparser.add_parser(
        'insert', help='Insert a note entry into a note'
    )
    add_parser.add_argument(
        'note', action='store', help='Note inserted into'
    )
    add_parser.add_argument('title', action='store', help='Notes title')

    # edit
    edit_parser = subparser.add_parser('edit', help='Edit a note entry')
    edit_parser.add_argument(
        'entry', action='store', type=int,
        help='Note entry index(integer) to edit'
    )
    edit_parser.add_argument('note', action='store', help='Note to be edited')

    # delete
    delete_parser = subparser.add_parser('delete', help='Delete a note')
    delete_parser.add_argument('note', action='store', help='Note to delete')

    # remove
    remove_parser = subparser.add_parser(
        'remove', help='Remove a note entry from a note'
    )
    remove_parser.add_argument(
        'entry', action='store',
        type=int, help='Note entry index(integer) to remove'
    )
    remove_parser.add_argument(
        'note', action='store', help='Note to remove from'
    )

    # move
    move_parser = subparser.add_parser(
        'move', help='Move a note entry from one note to another'
    )
    move_parser.add_argument(
        'entry', action='store',
        type=int, help='Note entry index(integer) to move'
    )
    move_parser.add_argument('fromnote', action='store')
    move_parser.add_argument('tonote', action='store')

    # add tags
    addtags_parser = subparser.add_parser(
        'addtags', help='Add tag(s) to a note'
    )
    addtags_parser.add_argument(
        'note', action='store', help='Note')
    addtags_parser.add_argument('tag', action='store', help='Tag(s)')

    # show tags
    tags_parser = subparser.add_parser(
        'tags', help='Show all the tags for a note'
    )
    tags_parser.add_argument('note', action='store', help='Note')

    # edit links
    editlink_parser = subparser.add_parser(
        'editlinks', help='Edit links for a note'
    )
    editlink_parser.add_argument('note', action='store', help='note')

    # show links
    links_parser = subparser.add_parser(
        'links', help='list all the links for a note'
    )
    links_parser.add_argument('note', action='store', help='note')

    # remove tags
    remove_parser = subparser.add_parser('removetags', help='Remove tag(s)')
    remove_parser.add_argument('note', action='store', help='Note')
    remove_parser.add_argument('tags', action='store', help='Tag(s)')

    # list
    list_parser = subparser.add_parser('list', help='List all notes')
    list_parser.add_argument(
        '--verbose', '-v', action='store_true', help='Verbose'
    )

    # display
    display_parser = subparser.add_parser(
        'display', help='Display a note content'
    )
    display_parser.add_argument('note', action='store', help='Note')
    display_parser.add_argument(
        '--short', '-s', action='store_true', help='short'
    )

    # showconfig
    showconfig_parser = subparser.add_parser(
        'showconfig', help='Show current configuration'
    )

    # setdefaultconfig
    setdefaultconfig_parser = subparser.add_parser(
        'setdefaultconfig', help='Reset to default configuration'
    )

    # setconfig
    setconfig_parser = subparser.add_parser(
        'setconfig', help='set a config option'
    )
    setconfig_parser.add_argument('key', action='store', help='Key')
    setconfig_parser.add_argument('value', action='store', help='Value')

    # search
    search_parser = subparser.add_parser('search', help='Regex search')
    search_parser.add_argument('regex', action='store', help='regex string')
    search_parser.add_argument(dest="note", action='store', help='note(s)')

    # check
    status_parser = subparser.add_parser(
        'check', help='check notes files and metadata for errors'
    )

    # interactive
    interactive_parser = subparser.add_parser(
        'interactive', help='interactive session'
    )

    # info lists python version and modues vesion for debugging
    info_parser = subparser.add_parser(
        'info', help='Info about notesviewer environment'
    )

    # parse user arguments
    args = vars(parser.parse_args())
    if args['cmd'] is None:
        notesviewer.file.print_err_msg("Missing command")
        parser.print_usage()
    process_args(args)


def process_args(argument):
    """ call the cm function for an arument """

    if argument['cmd'] == 'version':
        notesviewer.commands.cm_version()
    elif argument['cmd'] == 'info':
        notesviewer.commands.cm_info()
    elif argument['cmd'] == 'setdefaultconfig':
        notesviewer.commands.cm_setdefaultconfig()
    elif argument['cmd'] == 'setconfig':
        notesviewer.commands.cm_setconfig(argument['key'], argument['value'])
    elif argument['cmd'] == 'showconfig':
        notesviewer.commands.cm_showconfig()
    elif argument['cmd'] == 'init':
        notesviewer.commands.cm_init()
    elif argument['cmd'] == 'add_profile':
        notesviewer.commands.cm_add_profile(argument['profile'])
    elif argument['cmd'] == 'show_profiles':
        notesviewer.commands.cm_show_profiles()
    elif argument['cmd'] == 'switch_profile':
        notesviewer.commands.cm_switch_profile(argument['profile'])
    elif argument['cmd'] == 'profile':
        notesviewer.commands.cm_profile()
    elif argument['cmd'] == 'list':
        notesviewer.commands.cm_list(argument['verbose'])
    elif argument['cmd'] == 'add':
        notesviewer.commands.cm_add(argument['note'])
    elif argument['cmd'] == 'insert':
        notesviewer.commands.cm_insert(argument['note'], argument['title'])
    elif argument['cmd'] == 'edit':
        notesviewer.commands.cm_edit(argument['entry'], argument['note'])
    elif argument['cmd'] == 'delete':
        notesviewer.commands.cm_delete(argument['note'])
    elif argument['cmd'] == 'remove':
        notesviewer.commands.cm_remove(argument['entry'], argument['note'])
    elif argument['cmd'] == 'move':
        notesviewer.commands.cm_move(argument['entry'],
                                     argument['fromnote'],
                                     argument['tonote'])
    elif argument['cmd'] == 'addtags':
        notesviewer.commands.cm_addtags(argument['note'], argument['tag'])
    elif argument['cmd'] == 'tags':
        notesviewer.commands.cm_tags(argument['note'])
    elif argument['cmd'] == 'removetags':
        notesviewer.commands.cm_removetags(argument['note'],
                                           argument['tags'])
    elif argument['cmd'] == 'editlinks':
        notesviewer.commands.cm_editlinks(argument['note'])
    elif argument['cmd'] == 'links':
        notesviewer.commands.cm_links(argument['note'])
    elif argument['cmd'] == 'display':
        notesviewer.commands.cm_display(argument['note'],
                                        argument['short'])
    elif argument['cmd'] == 'search':
        notesviewer.commands.cm_search(argument['regex'], argument['note'])
    elif argument['cmd'] == 'check':
        notesviewer.commands.cm_check()
    elif argument['cmd'] == 'interactive':
        notesviewer.interactive.interactive()


if __name__ == '__main__':
    main()
