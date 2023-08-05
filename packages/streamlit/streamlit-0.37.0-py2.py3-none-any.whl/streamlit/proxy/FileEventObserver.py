# Copyright 2018 Streamlit Inc. All rights reserved.

"""Declares the FileEventObserver class, that watches the file system.


Why this file is so complex
---------------------------

1) The problem it's solving is non-trivial: we want to observe files, but only
while there's a browser attached to them. So we need to keep track of files
*and* browsers. But...

2) ...the watchdog module's API is really weird. And on top of it, it only
allows you to watch *folders*, not *files* (I believe this is due to a
limitation of the underlying Mac FSEvents system API).

3) We also want to make sure there is only 1 watchdog.observer.Observer, since
otherwise we end up with several threads running.

4) Finally, we want to abstract away all of the above into a simple API. That's
the ReportObserver class.


How these classes work together
-------------------------------

- FileEventObserver : each instance of this is able to observe a single
  files so long as there's a browser interested in it. This uses
  _MultiFileObserver to watch files.

- _MultiFileObserver : singleton that observes multiple files. It does this by
  holding a watchdog.observer.Observer object, and manages several
  _FolderEventHandler instances. This creates _FolderEventHandlers as needed,
  if the required folder is not already being observed. And it also tells
  existing _FolderEventHandlers which files it should be watching for.

- _FolderEventHandler : event handler from when a folder is modified. You can
  register files in that folder that you're interested in. Then this object
  listens to folder events, sees if registered files changed, and fires
  callbacks if so.

"""

# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
from streamlit.compatibility import setup_2_3_shims
setup_2_3_shims(globals())

import os

from streamlit.proxy import proxy_util
from watchdog import events
from watchdog.observers import Observer

from streamlit.logger import get_logger
LOGGER = get_logger(__name__)


class FileEventObserver(object):
    """Observes a single file on disk using watchdog"""

    @staticmethod
    def close_all():
        """Close the ReportObserver singleton."""
        file_observer = _MultiFileObserver.get_singleton()
        file_observer.close()
        LOGGER.debug('Observer closed')

    def __init__(self, file_path, on_file_changed):
        """Constructor.

        Arguments
        ---------
        file_path : str
            Absolute path of the file to observe.

        on_file_changed : callable
            Function to call when the file changes.

        """
        self._file_path = file_path

        file_observer = _MultiFileObserver.get_singleton()
        file_observer.observe_file(file_path, on_file_changed)
        LOGGER.debug('Observer created for %s', file_path)

    def close(self):
        """Stop observing the file system."""
        file_observer = _MultiFileObserver.get_singleton()
        file_observer.stop_observing_file(self._file_path)


class _MultiFileObserver(object):
    """Observes multiple files."""

    _singleton = None

    @classmethod
    def get_singleton(cls):
        """Return the singleton DeltaConnection object.

        Instantiates one if necessary.
        """
        if cls._singleton is None:
            LOGGER.debug('No singleton. Registering one.')
            _MultiFileObserver()

        return _MultiFileObserver._singleton

    # Don't allow constructor to be called more than once.
    def __new__(cls):
        """Constructor."""
        if _MultiFileObserver._singleton is not None:
            raise RuntimeError('Use .get_singleton() instead')
        return super(_MultiFileObserver, cls).__new__(cls)

    def __init__(self):
        """Constructor."""
        _MultiFileObserver._singleton = self

        # Map of folder_to_observe -> _FolderEventHandler.
        self._folder_handlers = {}

        # The Observer object from the Watchdog module. Since this class is
        # only instantiated once, we only have a single Observer in Streamlit,
        # and it's in charge of observing all paths we're interested in.
        self._observer = Observer()
        self._observer.start()  # Start observer thread.

    def is_observing_file(self, file_path):
        """Return whether the file is currently being observed."""
        folder_path = os.path.abspath(os.path.dirname(file_path))
        folder_handler = self._folder_handlers.get(folder_path)

        if folder_handler is None:
            return False

        return folder_handler.is_observing_file(file_path)

    def observe_file(self, file_path, callback):
        """Start observing a file.

        Parameters
        ----------
        file_path : str
            The full path of the file to observe.

        callback : callable
            The function to execute when the file is changed.

        """
        folder_path = os.path.abspath(os.path.dirname(file_path))
        folder_handler = self._folder_handlers.get(folder_path)

        if folder_handler is None:
            folder_handler = _FolderEventHandler()
            self._folder_handlers[folder_path] = folder_handler

            folder_handler.watch = self._observer.schedule(
                folder_handler, folder_path, recursive=False)

        folder_handler.add_file_change_listener(file_path, callback)

    def stop_observing_file(self, file_path):
        """Stop observing a file.

        Parameters
        ----------
        file_path : str
            The full path of the file to stop observing.

        """
        folder_path = os.path.abspath(os.path.dirname(file_path))
        folder_handler = self._folder_handlers.get(folder_path)

        if folder_handler is None:
            LOGGER.debug(
                'Cannot stop observing path, because it is already not being '
                'observed. %s', folder_path)
            return

        folder_handler.remove_file_change_listener(file_path)

        if not folder_handler.is_observing_files():
            self._observer.unschedule(folder_handler.watch)
            del self._folder_handlers[folder_path]

    def close(self):
        """Close this _FileObserver object forever."""
        if len(self._folder_handlers) != 0:
            self._folder_handlers = {}
            LOGGER.debug(
                'Stopping observer thread even though there is a non-zero '
                'number of event observers!')
        else:
            LOGGER.debug('Stopping observer thread')

        self._observer.stop()
        self._observer.join(timeout=5)


class _FolderEventHandler(events.FileSystemEventHandler):
    """Listen to folder events, see if certain files changed, fire callback.

    The super class, FileSystemEventHandler, listens to changes to *folders*,
    but we need to listen to changes to *files*. I believe this is a limitation
    of the Mac FSEvents system API, and the watchdog library takes the lower
    common denominator.

    So in this class we watch for folder events and then filter them based
    on whether or not we care for the file the event is about.
    """

    def __init__(self):
        """Constructor."""
        super(_FolderEventHandler, self).__init__()
        self._observed_files = {}

        # A watchdog.Watch instance.
        self.watch = None

    def add_file_change_listener(self, file_path, callback):
        """Add a file to this object's event filter.

        Parameters
        ----------
        file_path : str
        callback : Callable

        """
        if file_path in self._observed_files:
            LOGGER.debug('Already observing file: %s', file_path)
            return

        md5 = proxy_util.calc_md5_with_blocking_retries(file_path)
        modification_time = os.stat(file_path).st_mtime

        self._observed_files[file_path] = {
            'md5': md5,
            'modification_time': modification_time,
            'fn': callback,
        }

    def remove_file_change_listener(self, file_path):
        """Remove a file from this object's event filter.

        Parameters
        ----------
        file_path : str

        """
        if file_path not in self._observed_files:
            return

        del self._observed_files[file_path]

    def is_observing_file(self, file_path):
        """Return true if this object is observing the given file."""
        return file_path in self._observed_files

    def is_observing_files(self):
        """Return true if this object has 1+ files in its event filter."""
        return len(self._observed_files) > 0

    def handle_file_change_event(self, event):
        """Handle when file is changed.

        The events that can call this are modification, creation or moved
        events.

        Parameters
        ----------
        event : FileSystemEvent
            The event object representing the file system event.

        """
        if event.is_directory:
            return

        # Check for both modified and moved files, because many programs write
        # to a backup file then rename (i.e. move) it.
        if event.event_type == events.EVENT_TYPE_MODIFIED:
            file_path = event.src_path
        # On OSX with VI, on save, the file is deleted, the swap file is
        # modified and then the original file is created hence why we
        # capture EVENT_TYPE_CREATED
        elif event.event_type == events.EVENT_TYPE_CREATED:
            file_path = event.src_path
        elif event.event_type == events.EVENT_TYPE_MOVED:
            file_path = event.dest_path
        else:
            return

        if file_path not in self._observed_files:
            LOGGER.debug('Ignoring file %s', file_path)
            return

        file_info = self._observed_files[file_path]

        modification_time = os.stat(file_path).st_mtime
        if modification_time == file_info['modification_time']:
            LOGGER.debug('File timestamp did not change: %s', file_path)
            return

        file_info['modification_time'] = modification_time

        new_md5 = proxy_util.calc_md5_with_blocking_retries(file_path)
        if new_md5 == file_info['md5']:
            LOGGER.debug('File MD5 did not change: %s', file_path)
            return

        LOGGER.debug('File MD5 changed: %s', file_path)
        file_info['md5'] = new_md5
        file_info['fn']()

    def on_created(self, event):
        if event.is_directory:
            return
        self.handle_file_change_event(event)

    def on_modified(self, event):
        if event.is_directory:
            return
        self.handle_file_change_event(event)
