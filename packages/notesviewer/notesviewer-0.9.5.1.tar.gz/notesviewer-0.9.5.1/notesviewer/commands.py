""" commands module """

import sys
import uuid
import stat
import os
import shutil
from termcolor import colored
from notesviewer.config import showconfig, setdefaultconfig
import notesviewer.file
import notesviewer.error
import notesviewer.vardata
import notesviewer.note
import notesviewer.utils


def cm_version():
    """ print version """

    path = os.path.dirname(__file__)

    version = open(path + "/" + "_version").read()
    version = version.replace('\n', '')

    print(colored("Version is " + str(version),
                  notesviewer.vardata.OPTIONS['color_msg']))


def cm_init():
    """ initalize data """

    notesviewer.file.create_notes_root_path(
        notesviewer.vardata.PROFILE_NOTES_ROOT_PATH, "all")


def cm_add_profile(profile):
    """ create a new profile for """

    mode = 0o755 | stat.S_IRUSR

    profile_path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + profile

    try:
        os.makedirs(profile_path)
        os.makedirs(profile_path + "/" + "meta")
        os.makedirs(profile_path + "/" + "content")
        os.makedirs(profile_path + "/" + "tags")
        os.makedirs(profile_path + "/" + "link")
        notesviewer.file.print_info_msg(
            "initalized Root note directory... for " + "profile " + profile)
    except (OSError, FileExistsError):
        notesviewer.file.print_info_msg("Profile already exists")
        prompt_msg1 = "Would you like to initalize it again(yes/no)\n"
        prompt_msg2 = "This will also delete all your notes in your profile\n"

        prompt = input(prompt_msg1 + prompt_msg2)
        prompt = prompt.lower()
        if prompt == 'yes':
            shutil.rmtree(profile_path)
            os.makedirs(profile_path + "/" + "meta")
            os.makedirs(profile_path + "/" + "content")
            os.makedirs(profile_path + "/" + "tags")
            os.makedirs(profile_path + "/" + "link")
            notesviewer.file.print_info_msg("Notes directory re-initalized")


def cm_show_profiles():
    """ print number of profiles """

    profiles_path = notesviewer.vardata.NOTES_ROOT_PATH

    if len(os.listdir(profiles_path)) is int(0):
        notesviewer.file.print_info_msg("empty")

    profiles = os.listdir(profiles_path)

    for profile in profiles:
        notesviewer.file.print_info_msg(profile)


def cm_switch_profile(profile):
    """ switch to a profile """

    profile_path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + profile

    if not os.path.exists(profile_path):
        notesviewer.file.print_err_msg("The " + profile +
                                       " profile does not exist -- bye"
                                       )
        exit(notesviewer.error.ERROR_NO_PROFILE)

    notesviewer.config.setconfig("profile", profile)

    notesviewer.file.print_info_msg("Switched to " + profile)


def cm_profile():
    """ show current profile """

    notesviewer.file.print_info_msg(notesviewer.vardata.OPTIONS['profile'])


def cm_add(note):
    """add a note"""

    error_invalid_name_msg = note + " is not a valid note name. "
    error_invalid_name_msg2 = "Please choose a name with " + \
                              "these characters only: "

    # file permission
    mode = 0o600 | stat.S_IRUSR

    meta_path = notesviewer.file.getnotepath(note, "meta")
    content_path = notesviewer.file.getnotepath(note, "content")
    tag_path = notesviewer.file.getnotepath(note, "tag")
    link_path = notesviewer.file.getnotepath(note, "link")

    # create the note files
    if notesviewer.file.verify_note(note, "meta") is True:
        notesviewer.file.print_err_msg("The note " + note + " already exists")
        exit(notesviewer.error.ERROR_META_FILE_ALREADY_EXISTS)
    else:
        if not notesviewer.utils.validnotename(note):
            notesviewer.file.print_err_msg(error_invalid_name_msg +
                                           error_invalid_name_msg2 +
                                           notesviewer.vardata.APPROVED_CHARS
                                           )
            exit(notesviewer.error.ERROR_NOTE_INVALID_NOTE_CHARS)
        else:
            os.mknod(meta_path, mode)
            os.mknod(content_path, mode)
            os.mknod(tag_path, mode)
            os.mknod(link_path, mode)
            notesviewer.file.print_info_msg("Added " + note + " note")
            exit(notesviewer.error.ERROR_OK)


def cm_insert(note, title):
    """Insert a note with a title"""

    # verfiy note
    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg("The note " + note +
                                       "does not exist -- bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)
    if notesviewer.file.verify_note(note, "content") is False:
        notesviewer.file.print_msg("The " + note +
                                   "does not exist -- bye")
        exit(notesviewer.error.ERROR_NO_CONTENT_FILE)

    # create uuid for the note
    note_uuid = uuid.uuid4()

    # edit the file
    content = notesviewer.note.edit_file('')
    content = content[:-1]

    # convert the content into a string
    str_content = ""
    str_content = str_content.join(content)
    str_content = repr(str_content)
    str_content = str_content.replace("'", "")

    # open meta and content files
    fp_meta = notesviewer.file.open_note("meta", note, "a")
    fp_content = notesviewer.file.open_note("content", note, "a")

    # write to meta
    meta_buffer_string = "uuid:" + str(note_uuid) + " " + "title:" + title
    fp_meta.write(meta_buffer_string + "\n")

    # write to content
    content_buffer_string = "uuid:" + str(note_uuid) + " " + \
        "content:" + str_content
    fp_content.write(content_buffer_string + "\n")

    # close files
    notesviewer.file.close_note(fp_meta)
    notesviewer.file.close_note(fp_content)


def cm_edit(entry, note):
    """edit  a note entry"""

    # verfiy note
    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg("The meta note " + note + " \
                                            does not exist -- bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)
    if notesviewer.file.verify_note(note, "content") is False:
        notesviewer.file.print_msg("The content " + note + " \
                                            does not exist -- bye")
        exit(notesviewer.error.ERROR_NO_CONTENT_FILE)

    if notesviewer.utils.validate_content_index(entry, note) is False:
        print(colored("entry number is incorrect -- bye",
                      notesviewer.vardata.OPTIONS['color_err']))
        exit(notesviewer.error.ERROR_INVALID_INDEX)
    else:
        fp_content = notesviewer.file.open_note("content", note, "r")
        content_lines = fp_content.readlines()

        content_uuid = notesviewer.utils.getuuidbyindex(content_lines,
                                                        entry)
        content_string = notesviewer.utils.get_content_by_uuid(content_lines,
                                                               content_uuid)

        content_string = content_string.replace("\\n", "\n")
        content_string = notesviewer.note.edit_file(content_string)

        # remove newline and apostrophe
        char = content_string
        char = content_string.strip()
        char = repr(char)
        char = notesviewer.utils.remove_first_and_last_chars(char)

        # close fp
        notesviewer.file.close_note(fp_content)

        # fill content_lines to one that we edited
        content_lines[entry - 1] = \
            "uuid" + ":" + content_uuid + " " + "content" + ":" + char + "\n"

        # convert content_lines list to string
        str_content_lines = ""
        str_content_lines = str_content_lines.join(content_lines)

        # write back to content file
        fp_content = notesviewer.file.open_note("content", note, "w+")
        fp_content.write(str_content_lines)
        notesviewer.file.close_note(fp_content)


def cm_delete(note):
    """delete a note"""

    prompt_msg = "Are you sure you want to delete " + note + " (yes/no)"

    if notesviewer.file.verify_note(note, "meta") is False:
        error_msg = "The note " + note + " does not exist or is corrupted"
        notesviewer.file.print_err_msg(error_msg)
        exit(notesviewer.error.ERROR_NO_META_FILE)
    else:
        prompt = input(prompt_msg)

        prompt = prompt.lower()
        if prompt == "yes":
            os.remove(notesviewer.file.getnotepath(note, "meta"))
            if notesviewer.file.verify_note(note, "content") is True:
                os.remove(notesviewer.file.getnotepath(note, "content"))
                if notesviewer.file.verify_note(note, "link") is True:
                    os.remove(notesviewer.file.getnotepath(note, "link"))
                if notesviewer.file.verify_note(note, "tag") is True:
                    os.remove(notesviewer.file.getnotepath(note, "tag"))

            notesviewer.file.print_info_msg("Deleted " + note + " note")


def cm_remove(entry, note):
    """remove entry function"""

    meta_error_msg = "The note " + note + " does not exist or corrupted -- bye"
    content_error_msg = "The content " + note + \
                        " does not exist or corrupted -- bye"

    remove_msg = "Removed note entry " + str(entry) + \
                 " from " + note + " Note"

    remove_invalid_entry = "Invalid note entry " + str(entry) + " -- bye"

    # verfiy note and entry
    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg(meta_error_msg)
        exit(notesviewer.error.ERROR_NO_META_FILE)
    if notesviewer.file.verify_note(note, "content") is False:
        notesviewer.file.print_msg(content_error_msg)
        exit(notesviewer.error.ERROR_NO_CONTENT_FILE)
    if notesviewer.utils.validate_content_index(entry, note) is False:
        notesviewer.file.print_err_msg(remove_invalid_entry)
        exit(notesviewer.error.ERROR_INVALID_INDEX)

    else:
        fp_meta = notesviewer.file.open_note("meta", note, "r")
        fp_content = notesviewer.file.open_note("content", note, "r")
        meta_lines = fp_meta.readlines()
        content_lines = fp_content.readlines()
        uuid_meta = notesviewer.utils.getuuidbyindex(meta_lines, entry)
        uuid_content = notesviewer.utils.getuuidbyindex(content_lines,
                                                        entry)
        notesviewer.utils.removeuuidfromlist(meta_lines, uuid_meta)
        notesviewer.utils.removeuuidfromlist(content_lines, uuid_content)
        string_meta = ''.join(meta_lines)
        string_content = ''.join(content_lines)
        notesviewer.file.close_note(fp_meta)
        notesviewer.file.close_note(fp_content)

        # open files(content and meta) for writting
        fp_meta = notesviewer.file.open_note("meta", note, "w")
        fp_content = notesviewer.file.open_note("content", note, "w")
        fp_meta.write(string_meta)
        fp_content.write(string_content)
        notesviewer.file.close_note(fp_meta)
        notesviewer.file.close_note(fp_content)

        notesviewer.file.print_info_msg(remove_msg)

        exit(notesviewer.error.ERROR_OK)


def cm_move(entry, fromnote, tonote):
    """move an  entry from fromnote to tonote"""

    move_msg1 = "The note entry " + str(entry) + " at " + fromnote
    move_msg2 = " has been moved to " + tonote
    move_error1 = "The fromnote " + fromnote + " does not exist -- bye "
    move_error2 = "The tonote " + tonote + " does not exist -- bye "
    move_error3 = "The fromnote " + fromnote + " content does not exist -- bye"
    move_error4 = "The tonote " + tonote + " content does not exist -- bye"

    if notesviewer.file.verify_note(fromnote, "meta") is False:
        notesviewer.file.print_err_msg(move_error1)
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(tonote, "meta") is False:
        notesviewer.file.print_err_msg(move_error2)
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(fromnote, "content") is False:
        notesviewer.file.print_err_msg(move_error3)
        exit(notesviewer.error.ERROR_NO_CONTENT_FILE)

    if notesviewer.file.verify_note(tonote, "content") is False:
        notesviewer.file.print_err_msg(move_error4)
        exit(notesviewer.error.ERROR_NO_CONTENT_FILE)

    # validate note entry from fromnote
    if notesviewer.utils.validate_content_index(entry, fromnote) is False:
        print(colored("entry number is incorrect -- bye",
                      notesviewer.vardata.OPTIONS['color_err']))
        exit(notesviewer.error.ERROR_INVALID_INDEX)

    # open files(content and meta) for reading
    fp_meta_from = notesviewer.file.open_note("meta", fromnote, "r")
    fp_content_from = notesviewer.file.open_note("content", fromnote, "r")

    meta_lines = fp_meta_from.readlines()
    content_lines = fp_content_from.readlines()
    uuid_meta = notesviewer.utils.getuuidbyindex(meta_lines, entry)
    uuid_content = notesviewer.utils.getuuidbyindex(content_lines, entry)
    remove_note_meta = notesviewer.utils.removeuuidfromlist(meta_lines,
                                                            uuid_meta)
    remove_note_content = notesviewer.utils.removeuuidfromlist(content_lines,
                                                               uuid_content)
    string_meta = ''.join(meta_lines)
    string_content = ''.join(content_lines)
    notesviewer.file.close_note(fp_meta_from)
    notesviewer.file.close_note(fp_content_from)

    # open files(content and meta) for writting
    fp_meta_from = notesviewer.file.open_note("meta", fromnote, "w")
    fp_content_from = notesviewer.file.open_note("content", fromnote, "w")
    fp_meta_from.write(string_meta)
    fp_content_from.write(string_content)
    notesviewer.file.close_note(fp_meta_from)
    notesviewer.file.close_note(fp_content_from)

    # open meta and content files
    fp_meta = notesviewer.file.open_note("meta", tonote, "a")
    fp_content = notesviewer.file.open_note("content", tonote, "a")

    # write to meta
    fp_meta.write(remove_note_meta)

    # write to content
    fp_content.write(remove_note_content)

    notesviewer.file.print_info_msg(move_msg1 + move_msg2)

    # close files
    notesviewer.file.close_note(fp_meta)
    notesviewer.file.close_note(fp_content)


def cm_addtags(note, tag):
    """ adding tags to note file"""

    duplicate_tags = []

    # get all the tags
    tags = tag.split(',')

    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg(note + " Note does not exist -- bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(note, "tag") is False:
        notesviewer.file.print_err_msg(note + "Tag file does not exist -- bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)

    # read tags for existing tag
    fp_tags_read = notesviewer.file.open_note("tag", note, "r")
    lines = fp_tags_read.readlines()
    for line in lines:
        line = notesviewer.utils.remove_newline(line)
        for tag_index in tags:
            if tag_index == line:
                duplicate_tags.append(tag_index)
                break
    # close tag file
    notesviewer.file.close_note(fp_tags_read)

    # open tag file
    fp_tags = notesviewer.file.open_note("tag", note, "a")

    # write tag(s) to tag file
    for tag_index in tags:
        if notesviewer.utils.is_a_member_of_list(duplicate_tags, tag_index) \
           is True:
            print(colored(tag_index + " is already a tag",
                          notesviewer.vardata.OPTIONS['color_msg']))
        else:
            fp_tags.write(tag_index + "\n")
            notesviewer.file.print_info_msg("Added " +
                                            "#" + tag_index + " tag")
    # close tag file
    notesviewer.file.close_note(fp_tags)


def cm_tags(note):
    """show tags for a note"""

    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg(note + " Note does not exist --bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(note, "tag") is False:
        notesviewer.file.print_err_msg(note + " Tag file does not exist --bye")
        exit(notesviewer.error.ERROR_NO_TAG_FILE)

    if notesviewer.file.verify_empty_note(note, "tag") is True:
        notesviewer.file.print_info_msg("Note is empty")

    fp_tags = notesviewer.file.notesviewer.file.open_note("tag", note, "r")

    lines = fp_tags.readlines()
    for line in lines:
        line = "#" + line
        print(colored(line,
                      notesviewer.vardata.OPTIONS['color_msg']), end="")

    # if notesviewer.file.verify_empty_note(note, "tag") is False:
    # print("\n", end="")

    notesviewer.file.close_note(fp_tags)


def cm_removetags(note, tags):
    """ remove tag(s) for a note """

    removed_lines = []
    lines_without_newlines = []
    removed_tag_list = []

    tag_list = tags.split(',')

    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg(note + " Note does not exist --bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(note, "tag") is False:
        notesviewer.file.print_err_msg(note +
                                       " Note tag file does not exist --bye")
        exit(notesviewer.error.ERROR_NO_TAG_FILE)

    # open file and readlines
    fp_tags = notesviewer.file.open_note("tag", note, "r")
    lines = fp_tags.readlines()

    # remove newlines
    for line in lines:
        line = line.replace('\n', '')
        lines_without_newlines.append(line)

    for tag in tag_list:
        if tag in lines_without_newlines:
            removed_tag_list.append(tag)

    # move item's not to be removed
    for line in lines_without_newlines:
        # line = notesviewer.utils.remove_newline(line)
        if notesviewer.utils.is_a_member_of_list(tag_list, line) is False:
            removed_lines.append(line)

    # write to tag file
    fp_tags_removed = notesviewer.file.open_note("tag", note, "w")
    removed_tag_strings = '\n'.join(removed_lines)
    removed_tag_strings = removed_tag_strings + "\n"
    if removed_tag_strings == '\n':
        removed_tag_strings = ""

    fp_tags_removed.write(removed_tag_strings)

    # output message
    if not removed_tag_list:
        notesviewer.file.print_info_msg("No tags removed")
    elif len(removed_tag_list) == 1:
        notesviewer.file.print_info_msg(
            "Removed " + ','.join(removed_tag_list) + " tag")
    else:
        notesviewer.file.print_info_msg(
            "Removed " + ','.join(removed_tag_list) + " tags")

    # close files
    notesviewer.file.close_note(fp_tags)
    notesviewer.file.close_note(fp_tags_removed)


def cm_editlinks(note):
    """ Edit link for a note """

    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg(note + " Note does not exist --bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(note, "link") is False:
        notesviewer.file.print_err_msg(note + " Tag file does not exist --bye")
        exit(notesviewer.error.ERROR_NO_TAG_FILE)

    # open file and readlines
    fp_link = notesviewer.file.open_note("link", note, "r")
    lines = fp_link.readlines()

    # convert to string
    line_string = ''.join(lines)

    # edit links
    edited_link = notesviewer.note.edit_file(line_string)

    # close fp
    notesviewer.file.close_note(fp_link)

    if not notesviewer.note.check_links(edited_link):
        notesviewer.file.print_err_msg(
            "Unable to save some of the links --bye"
        )
    else:

        # write back to content file
        fp_link = notesviewer.file.open_note("link", note, "w+")
        fp_link.write(edited_link)
        notesviewer.file.close_note(fp_link)


def cm_links(note):
    """ show all the links for a note """

    if notesviewer.file.verify_note(note, "meta") is False:
        notesviewer.file.print_err_msg(note + " Note does not exist --bye")
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_note(note, "link") is False:
        notesviewer.file.print_err_msg(note + " Tag file does not exist --bye")
        exit(notesviewer.error.ERROR_NO_TAG_FILE)

    # open file and readlines
    fp_link = notesviewer.file.open_note("link", note, "r")
    lines = fp_link.readlines()

    if notesviewer.file.verify_empty_note(note, "link"):
        notesviewer.file.print_info_msg("Empty link")
        exit(notesviewer.error.ERROR_OK)

    # print all links
    notesviewer.file.print_list_per_line(lines, False)

    exit(notesviewer.error.ERROR_OK)


def cm_list(verbose):
    """ print name of the notes"""

    meta_path = notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "meta"

    if len(os.listdir(meta_path)) is int(0):
        notesviewer.file.print_info_msg("empty")

    notes = os.listdir(notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" +
                       "meta")
    if verbose is False:
        notesviewer.file.print_list_per_line(os.listdir(
            notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "meta"))

    else:
        for note in notes:
            if notesviewer.file.verify_empty_note(note, "meta") is True:
                notesviewer.file.print_msg(
                    notesviewer.vardata.OPTIONS['color_note'],
                    note + " " + "(empty)")
            else:
                path_meta = notesviewer.file.getnotepath(note, "meta")
                path_content = notesviewer.file.getnotepath(note,
                                                            "content")
                path_tags = notesviewer.file.getnotepath(note,
                                                         "tag")
                path_links = notesviewer.file.getnotepath(note,
                                                          "link")
                size_meta = os.stat(path_meta)
                size_content = os.stat(path_content)
                size_tags = os.stat(path_tags)
                size_link = os.stat(path_links)
                size_total = size_meta.st_size + \
                    size_content.st_size + \
                    size_tags.st_size + size_link.st_size
                notesviewer.file.print_msg(
                    notesviewer.vardata.OPTIONS['color_note'],
                    note + " (" + str(size_total) + "b)")

        if verbose is True:
            print(colored("---------",
                          notesviewer.vardata.OPTIONS['color_msg']))
            print(colored("Total notes: ",
                          notesviewer.vardata.OPTIONS['color_msg']), end="")
            notes_size = len(notes)
            print(colored(notes_size,
                          notesviewer.vardata.OPTIONS['color_msg']))


def cm_display(note, short):
    """display a note"""

    # Notes empty object
    class Notes:
        """ Class Notes """
        pass

    # note list
    notes = []
    index = 0

    if notesviewer.file.verify_note(note, "meta") is False:
        error_msg = "The note " + note + " does not exist -- bye"
        notesviewer.file.print_err_msg(error_msg)
        exit(notesviewer.error.ERROR_NO_META_FILE)

    if notesviewer.file.verify_empty_note(note, "meta"):
        notesviewer.file.print_info_msg("Empty note")
        exit(notesviewer.error.ERROR_OK)

    # open meta and content files
    fp_meta = notesviewer.file.open_note("meta", note, "r")
    fp_content = notesviewer.file.open_note("content", note, "r")

    # read files
    meta_lines = fp_meta.readlines()
    content_lines = fp_content.readlines()

    # loop over list and print
    for line in meta_lines:
        uuid = notesviewer.utils.get_uuid(line)
        uuid = uuid.split(":")[1]
        title = notesviewer.utils.get_title(line)
        title = notesviewer.utils.remove_newline(title)
        title = title.split(":")[1]
        content = notesviewer.utils.get_content_by_uuid(
            content_lines, uuid)
        notes.append(Notes())
        notes[index].uuid = uuid
        notes[index].title = title
        notes[index].content = content
        if short is True:
            print(index + 1, end="")
            print(" ", end="")
            print("-> ", end="")
            print(colored(title,
                          notesviewer.vardata.OPTIONS['color_title']))
        else:
            # print("----------")
            print(str(index + 1) + ") ", end="")
            print(">>> " + colored(notes[index].title,
                                   notesviewer.vardata.OPTIONS['color_title']))
            notesviewer.utils.print_content(notes[index].content)
        index = index + 1

    # close files
    notesviewer.file.close_note(fp_meta)
    notesviewer.file.close_note(fp_content)


def cm_search(regex, note):
    """main search function"""

    # index for search starts at 1
    index = 1

    # by defatul set it true
    search_all_notes = True

    # split note argument by comma into notes
    # n = note[0]
    notes = note.split(",")

    # cheking for multiple argument with all
    if len(notes) > 1:
        for i in notes:
            if i == "all":
                notesviewer.file.print_err_msg(
                    "Ambiguity between all and notes")
                exit(notesviewer.error.ERROR_SEARCH_NOTE_AMBIGUITY)
            elif notesviewer.file.verify_note(i, "meta") is False:
                notesviewer.file.print_err_msg(
                    "The note " + i + " does not exist -- bye")
                exit(notesviewer.error.ERROR_NO_META_FILE)

    # check and set the search_all_notes
    else:
        if notes[0] == "all":
            search_all_notes = True

        else:
            search_all_notes = False
            if notesviewer.file.verify_note(note, "meta") is False:
                notesviewer.file.print_err_msg(
                    "The note " + note + " does not exist -- bye")
                exit(notesviewer.error.ERROR_NO_META_FILE)

    # if we choose all notes
    if search_all_notes is True:
        notes = notesviewer.utils.get_all_notes(True)

    # load notes info and split if multi line enteries
    notes_info = notesviewer.note.load_notes_enteries(notes)
    notes_info = notesviewer.note.split_multline_note_enteries(notes_info)

    # regex the string
    searches = notesviewer.utils.regex_string(notes_info, regex)

    # print output
    for i in searches:
        print(str(index) + ")", end='')
        notesviewer.utils.print_search_line(i)
        note_name = notesviewer.utils.get_note_name(i[3])
        print("("
              + colored(note_name,
                        notesviewer.vardata.OPTIONS['color_search_notename']) +
              ")")
        index = index + 1

    if index == 1:
        notesviewer.file.print_info_msg("No Results")


def cm_check():
    """ command to verify notes """

    print("Checking root folders..")

    errors = notesviewer.file.verify_profile_path(True)
    if notesviewer.error.ERROR_META_MISSING in errors:
        exit(notesviewer.error.ERROR_META_MISSING)

    notes = os.listdir(notesviewer.vardata.PROFILE_NOTES_ROOT_PATH +
                       "/" + "meta")

    print()
    print("Checking note files")
    if not notes:
        notesviewer.file.print_info_msg("Empty")
        exit(notesviewer.error.ERROR_OK)
    for note in notes:
        status = notesviewer.note.inspect_note(note)
        print("Checking " + note)

        if status['meta'] is True:
            notesviewer.file.print_info_msg("meta..OK")
        else:
            notesviewer.file.print_err_msg('meta..MISSING')

        if status['content'] is True:
            notesviewer.file.print_info_msg("content..OK")
        else:
            notesviewer.file.print_err_msg('content..MISSING')

        if status['link'] is True:
            notesviewer.file.print_info_msg("link..OK")
        else:
            notesviewer.file.print_err_msg('link..MISSING')

        if status['tags'] is True:
            notesviewer.file.print_info_msg("tags..OK")
        else:
            notesviewer.file.print_err_msg('tags..MISSING')

    print()

    # check for index mismatch
    print("Chekcing notes metadata..")
    for note in notes:
        print("checking " + note)
        # ignore empty notes
        if notesviewer.file.verify_empty_note(note, "meta") is True:
            notesviewer.file.print_info_msg(note + "(Ignoring ..empty)")
            continue
        meta_uuid, content_uuid = notesviewer.note.get_note_uuids(note)
        meta_size = len(meta_uuid)
        content_size = len(content_uuid)
        if meta_size == content_size:
            for index in range(meta_size):
                if meta_uuid[index] == content_uuid[index]:
                    notesviewer.file.print_info_msg(
                        meta_uuid[index] + "..,passed")
                else:
                    notesviewer.file.print_err_msg(
                        meta_uuid[index] + "...not passed")
        else:
            notesviewer.file.print_err_msg("Note entry mismatch")


def cm_showconfig():
    """show config"""

    showconfig()


def cm_setconfig(key, value):
    """ set config for key:value"""

    notesviewer.config.setconfig(key, value)


def cm_info():
    """info display pyton and modueles version"""

    print("Major Version:" + str(sys.version_info.major))
    print("Minor Version:" + str(sys.version_info.minor))
    print("Micro Version:" + str(sys.version_info.micro))
    print("Release Version:" + str(sys.version_info.releaselevel))
    print("Serial Release number:" + str(sys.version_info.serial))
    print(sys.version)
    print("Platform:" + sys.platform)
    print("Os name:" + os.name)


def cm_setdefaultconfig():
    """ command to set default config """
    setdefaultconfig(True)
