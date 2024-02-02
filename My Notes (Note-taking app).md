Maybe: Shortcuts should be easily customizable. 
 Or not. Emacs doesn't.

Remove secondary menu bar TODO

TODO add home menu above file menu

Should I have used a declarative language?

Reason to not copy and paste code verbatim:

    It may not be readable to you. It may be too verbose. The code should be customize     to you / your program

- [x] Replace update_title() with self.setWindowTitle(f"{self.title} - QuickNote")

- [x] Save title in json

- [x] try out tableView instead of gridLayout (not essential though)

- [ ] Add delete entries functionality (soft delete (flag to hide entry (record)))

- [x] Figure out pyinstaller with json file

- [x] Use QListWidget instead of QGridLayout (for keyboard navigatability)



keypressevent doesn't work after adding qlistwidget. 

This was a real headache.

    It's because there was focus was on qlistwidget. It's weird but that's how key press event works. So I had to use QShortcut. Works for "n" and "q" but not for "Return". That needs to be addressed.