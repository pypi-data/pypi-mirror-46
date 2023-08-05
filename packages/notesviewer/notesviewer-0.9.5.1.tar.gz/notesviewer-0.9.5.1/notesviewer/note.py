"""note module """

import subprocess
import tempfile
import os
import notesviewer.utils
import notesviewer.file
import notesviewer.vardata


def edit_file(content):
    """open a file and return result"""

    # Get the user's editor
    editor = notesviewer.vardata.OPTIONS['editor']

    # Open the content with a temp file and send the reult back
    with tempfile.NamedTemporaryFile("a+") as tmpfile:
        tmpfile.write(content)
        tmpfile.flush()
        subprocess.check_call([editor, tmpfile.name])
        tmpfile.seek(0)
        output = tmpfile.read()

    return output


def load_notes_enteries(notes):
    """load list of notes into memory"""

    index = 0

    class Notes:
        """Class docstring"""
        pass

    all_notes_enteries = []

    for note in notes:

        meta_path = notesviewer.file.getnotepath(note, "meta")
        content_path = notesviewer.file.getnotepath(note, "content")

        if os.path.getsize(meta_path) > 0:
            fp_meta = notesviewer.file.open_note("meta", note, "r")
            meta_lines = fp_meta.readlines()
        if os.path.getsize(content_path) > 0:
            fp_content = notesviewer.file.open_note("content", note, "r")
            content_lines = fp_content.readlines()

            for meta_line in meta_lines:
                uuid = notesviewer.utils.get_uuid(meta_line)
                uuid = uuid.split(":")[1]
                title = notesviewer.utils.get_title(meta_line)
                title = title.split(":")[1]
                title = notesviewer.utils.remove_newline(title)
                content = notesviewer.utils.get_content_by_uuid(content_lines,
                                                                uuid)
                content = notesviewer.utils.remove_newline(content)
                all_notes_enteries.append(Notes())
                all_notes_enteries[index].uuid = uuid
                all_notes_enteries[index].title = title
                all_notes_enteries[index].note = note
                all_notes_enteries[index].content = content
                index = index + 1

    return all_notes_enteries


def split_multline_note_enteries(notes):
    """ if notes have multiple line split them into seperate enteries"""

    class Notes:
        """ Class note """
        pass

    splited_notes = []

    splited_index = 0
    for note in notes:
        content = note.content.split('\\n')
        if len(content) > 1:
            for c_index in content:
                splited_notes.append(Notes())
                splited_notes[splited_index].uuid = note.uuid
                splited_notes[splited_index].title = note.title
                splited_notes[splited_index].note = note.note
                splited_notes[splited_index].content = c_index
                splited_index = splited_index + 1
        else:
            splited_notes.append(Notes())
            splited_notes[splited_index].uuid = note.uuid
            splited_notes[splited_index].title = note.title
            splited_notes[splited_index].note = note.note
            splited_notes[splited_index].content = note.content
            splited_index = splited_index + 1

    return splited_notes


def inspect_note(note):
    """ check note for any inconsistencies or corruption"""

    note_error = {'meta': True, 'content': True, 'link': True, 'tags': True}

    note_error['meta'] = notesviewer.file.verify_note(note, "meta")
    note_error['content'] = notesviewer.file.verify_note(note, "content")
    note_error['link'] = notesviewer.file.verify_note(note, "link")
    note_error['tags'] = notesviewer.file.verify_note(note, "tag")

    return note_error


def get_note_uuids(note):
    """ check index between meta and content """

    meta_uuid = []
    content_uuid = []

    meta_fp = notesviewer.file.open_note("meta", note, "r")
    content_fp = notesviewer.file.open_note("content", note, "r")

    meta_lines = meta_fp.readlines()
    content_lines = content_fp.readlines()

    for line in meta_lines:
        m_uuid = notesviewer.utils.get_uuid(line)
        m_uuid = m_uuid.split(":")[1]
        meta_uuid.append(m_uuid)

    for line in content_lines:
        c_uuid = notesviewer.utils.get_uuid(line)
        c_uuid = c_uuid.split(":")[1]
        content_uuid.append(c_uuid)

    notesviewer.file.close_note(meta_fp)
    notesviewer.file.close_note(content_fp)

    return meta_uuid, content_uuid


def check_links(note_string):
    """ check links for any issues """

    # convert to list
    note_list = note_string.split()

    # verify all the links
    for link in note_list:
        if not verify_link(link):
            return False
    return True


def verify_link(link):
    """ verify a link for correctness """

    # get the protocol from link string
    link_parts = link.split(":")
    if link_parts[0] == 'http':
        return True
    if link_parts[0] == 'https':
        return True
    return False
