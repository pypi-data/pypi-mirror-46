=============
macos_display
=============

Fetch information about macOS displays given a display ID, which is available from
``nsscreen.deviceDescription()["NSScreenNumber"]`` using pyobjc.

Get the user-visible display name from an id::

  >>> import macos_display
  >>> macos_display.display_name(69732928)
  'Color LCD'

List all display names::

  >>> from AppKit import NSScreen
  >>> import macos_display
  >>> screens = NSScreen.screens()
  >>> for screen in screens:
  ...     screen_id = screen.deviceDescription()["NSScreenNumber"]
  ...     name = macos_display.display_name(screen_id)
  ...     print(name)
  ... 
  Color LCD
  SAMSUNG
  LCD1970NXp
