# notesviewer

A commandline notes viewer written in python

## installation

pip install notesviewer

## usage

```
notesviewer --help
notesviewer version 
notesviewer list
notesviewer display <note> 
notesviewer add <note>
notesviewer insert <note> <title>
nosteviewer edit   <index> <note>
notesviewer delete <note>
notesviewer remove <index> <note>
notesviewer move <index> <fromnote> <tonote>
notesviewer addtags <note> <tag>
notesviewer add_profile <profile>
notesviewer show_profiles
notesviewer switch_profile
notesviewer profile
notesviewer tags <note>
notesviewer removetags <note> <tag(s)>
notesviewer editlinks <note>
notesviewer links <note>
notesviewer editlinks <note>
notesviewer showconfig
notesviewer setdefaultconfig
notesviewer setconfig <key> <value>
notesviewer search <regex> note(s)
notesviewer check
notesviewer interactive    #Not implemented yet

```

## changelog
```
0.9.3
- Changed parser argument for add,insert, delete, remove from name to note for consistency 
- Added help context to commands when using notesviewer --help

0.9.4
- Added links and editlinks commands for managing notes bookmarks(links)
- Added setconfig command to easily changing config settings
- Added root note verification
- Updated the check command to include the new root note verification
- Fixed --help to display notesviewer name correctly

0.9.5
- Changed the default editor to vi
- Added cyan, magenta and grey color options
- Changed some of the default colors
- Added note naming convention with approved characters
- Fixed display command bug when inserting with : character
- Notes root path and config are in the same location now
- Added profile, add_profile, show_profies, switch_profile commands for profile managment

0.9.5.1
- A default profile is created upon initalization
- Will Create a the profile path from config if missing

```

## Contributing 
Pull requests are welcome. 

## License 
GPL2
