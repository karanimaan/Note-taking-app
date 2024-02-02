# QuickNote

QuickNote is a note taking app, made for efficient usability. For one, using the keyboard to navigate is faster than using the mouse. Also it should be stable and predictable; therefore it should be plain text (using markdown or org mode). At the same time, it should be compatible with traditional paradigms (like using the mouse).

## Features

- Notes can be made quickly (without a filename)
- It must be fully navigable with the keyboard

## PyInstaller

This section explains how to create a binary from source. Windows binaries can be found on the Releases page.

PyInstaller bundles a Python application and all its dependencies into a single package. Make sure you have the [Requirements](https://pyinstaller.org/en/stable/requirements.html#pyinstaller-requirements) installed, and then install PyInstaller from PyPI:

```
pip install -U pyinstaller
```

Open terminal and navigate to the directory where *quick-note.py* file is located, then build the app with the following command:

```
pyinstaller quick-note.py
```

The bundled application should now be available in the _dist_ folder.

Have a look at https://pyinstaller.org/ for more information.
