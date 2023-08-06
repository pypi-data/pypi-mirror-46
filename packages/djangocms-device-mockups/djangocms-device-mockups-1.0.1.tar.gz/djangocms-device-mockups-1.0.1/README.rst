Django Device Mockups
========================

An extension for Django CMS that adds the Device Mockups CSS library to elements on DjangoCMS.

Installation
------------

1. Install with pip ``pip install djangocms-device-mockups``

2. Add ``djangocms_device_mockups`` to INSTALLED_APPS

3. Run migrations ``python manage.py migrate``


Usage
-----
See notes here:
https://github.com/pixelsign/html5-device-mockups

After installation simply add the plugins to the page.

Notes
-----
* If putting onto a background, ensure the background has both ``position`` and ``z-index`` < -1.

* Main CSS will limit device size to 300px, set ``.device-wrapper { max-width: 100%; ..}`` to make it responsive/resize etc.