"""
utils module
"""

import os
import re
from termcolor import colored
import notesviewer.vardata
import notesviewer.file


def getpath(name):
    """ get notes root path """
    return notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + name


def is_a_member_of_list(ali, item):
    """ utility function to see if item is member of a list"""

    is_a_member = False

    for i in ali:
        if i == item:
            is_a_member = True
            break

    return is_a_member


def get_note_name(uuid):
    """ get note's name """

    notes = get_all_notes(ignore_empty=False)

    for note in notes:
        meta_fp = notesviewer.file.open_note("meta", note, "r")
        meta_lines = meta_fp.readlines()

        for line in meta_lines:
            uid = get_uuid(line)
            uid = uid.split(":")[1]
            if uid == uuid:
                meta_fp.close()
                return note

        # close files
        notesviewer.file.close_note(meta_fp)

    return False


def get_all_notes(ignore_empty=False):
    """return a list of all notes from meta"""

    notes = os.listdir(
        notesviewer.vardata.PROFILE_NOTES_ROOT_PATH + "/" + "meta"
    )

    # remove the empty file from the notes list if we choose igonore
    if ignore_empty is True:
        for note in notes:
            if os.stat(
                    notesviewer.vardata.PROFILE_NOTES_ROOT_PATH
                    + "/" + "meta" + "/" + note).st_size == 0:
                notes.remove(note)

    return notes


def get_uuid(astr):
    """ return uuid from a string """
    return astr.split(" ", 1)[0]


def get_title(astr):
    """ return title from a string """
    return astr.split(" ", 1)[1]


def get_content(astr):
    """ return content from a string """
    return astr.split(" ", 1)[1]


def get_content_by_uuid(content_lines, uuid):
    """return a uuid from content_lines"""

    for line in content_lines:
        uid = get_uuid(line)
        uid = uid.split(":")[1]
        if uid == uuid:
            content = get_content(line)
            content = content.split(":", 1)[1]
            return content
    return 0


def remove_newline(astr):
    """ remove newline from a stirng"""
    return astr.replace("\n", "")


def remove_first_and_last_chars(astr):
    """remove first and last chars"""

    astr = astr[1:]
    astr = astr[:-1]
    return astr


def removeuuidfromlist(lines, uuid):
    """remove uuid line from list"""

    for i, line in enumerate(lines):
        line = get_uuid(line)
        line = line.split(":")[1]
        if line == uuid:
            note = lines.pop(i)
            return note

    return False


def print_search_line(search_line):
    """print search line"""

    index = 0
    content = search_line[2]

    for char in content:
        print_char(char, index, search_line)
        index = index + 1


def print_char(char, index, search_line):
    """print a char match"""

    inside = False
    matches = get_searches_per_line(search_line)

    for i in range(matches):
        begin = i * 4
        end = (i * 4) + 1

        if index >= search_line[begin]:
            if index <= search_line[end]:
                inside = True
                break

    if inside is True:
        print(colored(char,
                      notesviewer.vardata.OPTIONS['color_search_string']),
              end="")
    if inside is False:
        print(char, end="")


def print_content(content_line):
    """print content of a note"""

    newline = content_line.split("\\n")
    for i in newline:
        print(colored(i, notesviewer.vardata.OPTIONS['color_content']))


def get_searches_per_line(line):
    """ get searches per line """
    return len(line) // 4


def get_search_number_line(line):
    """get searcg per number line """
    size = get_searches_per_line(line)
    search_index = size - 1
    search_index = search_index * 3
    return(line[search_index], line[search_index + 1], line[search_index + 2])


def validate_content_index(index, name):
    """validate an index for a note"""

    meta_fp = notesviewer.file.open_note("meta", name, "r")
    lines = meta_fp.readlines()

    i = 0
    for line in lines:
        i = i + 1

    notesviewer.file.close_note(meta_fp)

    if 1 <= index <= i:
        return True
    return False


def getuuidbyindex(lines, index):
    """get uuid for a index into list"""

    ctr = 1
    for line in lines:
        if ctr == index:
            line = get_uuid(line)
            line = line.split(":")[1]
            return line
        ctr = ctr + 1

    return False


def regex_string(note_enteries, regex):
    """regex notes_eneries"""

    search_list = []
    search_lists = []

    # loop over not enteries
    for note_entry in note_enteries:
        del search_list[:]
        for match in re.finditer(regex, note_entry.content):
            start = match.start()
            end = match.end()
            search_list.append(start)
            search_list.append(end)
            search_list.append(note_entry.content)
            search_list.append(note_entry.uuid)
        if search_list:
            search_lists.append(list(search_list))

    return search_lists


def validnotename(note):
    """ check if a note's name has valid characters """

    for char in note:
        if char not in notesviewer.vardata.APPROVED_CHARS:
            return False
    return True
