## v1.3.7.beta ()
VERSION IN DEVELOPMENT

## v1.3.6 (2017/06/23)
Adds build settings for mac os and windows binaries
Adds requirements for releasing master versions (useful for building binaries)
Improves documentation for building binaries locally

## v1.3.5 (2017/06/21)
Improves documentation
Updates default logging settings
Uses a single logger for all libraries
Support for latest changes on pybranch library
Simplifies project installation from source (for developers)

## v1.3.4 (2017/05/04)
Adds support for new pybpod default plugin (pybpod-gui-plugin-session-history)
Enhances EventOccurrence messages handling
Fixes issue #5

## v1.3.3 (2017/05/03)
Fixes import task bugs
Enhances API exceptions
Show error if user tries to open invalid project
Fixes error deleting task closes app (PyForms)

## v1.3.2 (2017/04/28)
Fixes projects window incompatibility with other plugins
Adds support for live event occurrences (pybpod-api)
Adds support for handling erros on project opening
Raise error when project is open without a valid settings path
Adds support for closing project on background (without user prompt confirmation). This is useful for error handling.
Handle invalid user settings file without closing app (pyforms-generic-editor)
Handle invalid session files without closing app (pyforms-generic-editor)


## v.1.3.1.beta (2017/04/18)
Improves Mac OS build script (pyforms-generic-editor)
Fixes problem for editing user settings inside the app when in Mac OS bundle (pyforms-generic-editor)
Prompts for saving project changes when choosing quit option on menu (pyforms-generic-editor)
Adds support for editing user settings inside the app (pyforms-generic-editor)
Prompts for saving project changes on main window exit (pyforms-generic-editor)

## v.1.3.0.beta (2017/04/17)
Fixes plugins finder dev mode

## v.1.2.0 (2017/04/13)
Adds support for mac os and windows executables generation
Fixes Issue #2: Create new project
Use pyforms as package finder
Enhances README and frontpage photo

## v.1.1.0 (2017/04/04)
Adds support for Qt5

## v.1.0.0 (2017/03/23)
Release of beta version already working with pyforms_generic_editor
