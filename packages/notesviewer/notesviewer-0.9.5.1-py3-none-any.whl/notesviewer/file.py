""" Module file """

import os
import stat
import shutil
from termcolor import colored
import notesviewer.vardata
import notesviewer.error

MODES = ("r", "w", "a", "w+")


def open_note(file_context, note, mode):
    """open the meta and return a a fp"""

    # set the path for file_context
    if file_context == 'meta':
        path = notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "meta" + "/" + note
    elif file_context == 'content':
        path = notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "content" + "/" + note
    elif file_context == 'link':
        path = notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "link" + "/" + note
    elif file_context == 'tag':
        path = notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "tags" + "/" + note
    else:
        return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT

    if mode not in MODES:
        return notesviewer.error.ERROR_WRONG_MODE

    fileptr = open(path, mode)

    if fileptr is None:
        print(colored("Error while trying to open " + note + " --bye",
                      notesviewer.vardata.OPTIONS['color_err']))

    return fileptr


def close_note(filepointer):
    """ close a file pointer"""
    filepointer.close()


def create_config_file():
    """ create config file """

    mode = 0o600 | stat.S_IRUSR

    if not os.path.exists(notesviewer.vardata.ROOT):
        os.mkdir(notesviewer.vardata.ROOT)

    error = os.mknod(notesviewer.vardata.CONFIG_FILE_PATH, mode)
    if error is not None:
        print_err_msg("There was error creating config file " +
                      notesviewer.vardata.CONFIG_FILE_PATH)
        exit(-1)
    else:
        notesviewer.commands.setdefaultconfig(False)


def create_notes_root_path(profile_path, metadata_dir, prompt=True):
    """ creat a note root directory """

    mode = 0o755 | stat.S_IRUSR

    try:
        if metadata_dir == "all":
            os.makedirs(profile_path + "/" + "meta")
            os.makedirs(profile_path + "/" + "content")
            os.makedirs(profile_path + "/" + "tags")
            os.makedirs(profile_path + "/" + "link")
        if metadata_dir == "meta":
            os.makedirs(profile_path + "/" + "meta")
        if metadata_dir == "content":
            os.makedirs(profile_path + "/" + "content")
        if metadata_dir == "link":
            os.makedirs(profile_path + "/" + "link")
        if metadata_dir == "tags":
            os.makedirs(profile_path + "/" + "tags")
    except OSError:
        notesviewer.file.print_info_msg("Note directory already exists")
        prompt_msg1 = "Would you like to initalize it again(yes/no)\n"
        prompt_msg2 = "This will delete all your notes: "

        prompt = input(prompt_msg1 + prompt_msg2)
        prompt = prompt.lower()
        if prompt == 'yes':
            shutil.rmtree(notesviewer.vardata.PROFILE_NOTES_ROOT_PATH)
            os.makedirs(profile_path + "/" + "meta")
            os.makedirs(profile_path + "/" + "content")
            os.makedirs(profile_path + "/" + "tags")
            os.makedirs(profile_path + "/" + "link")
            notesviewer.file.print_info_msg("Notes directory re-initalized")


def verify_note(note, file_context):
    """ check note """

    path = getnotepath(note, file_context)
    if os.path.exists(path):
        return True
    return False


def verify_profile_path(verbose=False):

    """ check PROFILE_NOTES_ROOT_PATH folder and it's metadata exists"""

    no_root_msg = "No root note directory found"
    run_init_msg = "Use the init command to initalize Notes"
    metadata_msg = "Some of the metadata in notes directory are missing"
    metadata_msg3a = "..Run   " + notesviewer.vardata.PROGRAM_NAME + " check"
    metadata_msg3b = " command  to check what's missing or"
    metadata_msg4a = "..Run   " + notesviewer.vardata.PROGRAM_NAME + " init"
    metadata_msg4b = " command   to initalize base metadata directories"

    if not os.path.exists(notesviewer.vardata.PROFILE_NOTES_ROOT_PATH):
        return notesviewer.error.ERROR_NO_ROOT_NOTE

    # This will be called by cm_check

    missing = []
    if not os.path.exists(getrootpath("meta")):
        if verbose:
            notesviewer.file.print_err_msg("Meta folder missing")
        missing.append(notesviewer.error.ERROR_META_MISSING)
    else:
        if verbose:
            notesviewer.file.print_info_msg("Meta folder OK")
        missing.append(notesviewer.error.ERROR_OK)
    if not os.path.exists(getrootpath("content")):
        if verbose:
            notesviewer.file.print_err_msg("Content folder missing")
        missing.append(notesviewer.error.ERROR_CONTENT_MISSING)
    else:
        if verbose:
            notesviewer.file.print_info_msg("Content folder OK")
        missing.append(notesviewer.error.ERROR_OK)
    if not os.path.exists(getrootpath("link")):
        if verbose:
            notesviewer.file.print_err_msg("Link folder missing")
        missing.append(notesviewer.error.ERROR_LINK_MISSING)
    else:
        if verbose:
            notesviewer.file.print_info_msg("Link folder OK")
        missing.append(notesviewer.error.ERROR_OK)
    if not os.path.exists(getrootpath("tag")):
        if verbose:
            notesviewer.file.print_err_msg("tags folder missing")
        missing.append(notesviewer.error.ERROR_TAGS_MISSING)
    else:
        if verbose:
            notesviewer.file.print_info_msg("Tags folder OK")
        missing.append(notesviewer.error.ERROR_OK)

    return missing


def verify_empty_note(note, file_context):
    """ check note if empty """

    if os.stat(getnotepath(note, file_context)).st_size == 0:
        return True
    return False


def getnotepath(note, file_context):
    """ return note's path by file_context"""

    if file_context == 'meta':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "meta" + "/" + note
    if file_context == 'content':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "content" + "/" + note
    if file_context == 'link':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH +  \
            "/" + "link" + "/" + note
    if file_context == 'tag':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + \
            "/" + "tags" + "/" + note
    return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT


def getrootpath(file_context):
    """ return notes root path by file context """

    if file_context == 'meta':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "meta"
    if file_context == 'content':
        return  \
            notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "content"
    if file_context == 'link':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "link"
    if file_context == 'tag':
        return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "tags"
    return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT


def print_msg(color, msg):
    """ print msg at color base """

    print(colored(msg, color))


def print_err_msg(msg):
    """ print error msg with correct color"""

    print(colored(msg, notesviewer.vardata.OPTIONS['color_err']))


def print_info_msg(msg):
    """ print info msg with correct color"""

    print(colored(msg, notesviewer.vardata.OPTIONS['color_msg']))


def print_list_per_line(mylist, extra_line=True):
    """print a list"""

    if extra_line is False:
        for index in mylist:
            print(
                colored
                (index, notesviewer.vardata.OPTIONS['color_msg']),
                end="")
        return

    for index in mylist:
        print(colored(index, notesviewer.vardata.OPTIONS['color_note']))
