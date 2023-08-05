# Copyright 2018 Streamlit Inc. All rights reserved.

"""Exports everything that should be visible to Streamlit users.

The functions in this package wrap member functions of DeltaGenerator, as well
as from any namespace within DeltaGenerator. What they do is get the
DeltaGenerator from the singleton connection object (in streamlit.connection)
and then call the corresponding function on that DeltaGenerator.
"""

# NOTE: You'll see lots of "noqa: F821" in this file. That's because we
# manually mess with the local namespace so the linter can't know that some
# identifiers actually exist in the namespace.

# Python 2/3 compatibility
from __future__ import print_function, division, unicode_literals, absolute_import
from streamlit.compatibility import setup_2_3_shims
setup_2_3_shims(globals())

# Give the package a version.
import pkg_resources
import uuid

# This used to be pkg_resources.require('streamlit') but it would cause
# pex files to fail. See #394 for more details.
__version__ = pkg_resources.get_distribution('streamlit').version

# Deterministic Unique Streamlit User ID
# The try/except is needed for python 2/3 compatibility
try:
    __installation_id__ = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.getnode())))
except UnicodeDecodeError:
    __installation_id__ = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.getnode()).encode('utf-8')))

# Must be at the top, to avoid circular dependency.
from streamlit import logger
from streamlit import config
logger.set_log_level(config.get_option('global.logLevel').upper())
logger.init_tornado_logs()
LOGGER = logger.get_logger('root')

import contextlib
import functools
import re
import sys
import textwrap
import threading
import traceback
import types

from streamlit.DeltaConnection import DeltaConnection
from streamlit.DeltaGenerator import DeltaGenerator
from streamlit.caching import cache  # Just for export.
from streamlit import util


this_module = sys.modules[__name__]

# This delta generator has no queue so it can't send anything out on a
# connection.
_NULL_DELTA_GENERATOR = DeltaGenerator(None)

_DATAFRAME_LIKE_TYPES = (
    'DataFrame',  # pandas.core.frame.DataFrame
    'Series',  # pandas.core.series.Series
    'Index',  # pandas.core.indexes.base.Index
    'ndarray',  # numpy.ndarray
    'Styler',  # pandas.io.formats.style.Styler
)


def _with_dg(method):
    @functools.wraps(method)
    def wrapped_method(*args, **kwargs):
        # If we're unit testing, control the queue and don't make a
        # connection.
        if config.get_option('global.unitTest'):
            from streamlit.ReportQueue import ReportQueue
            delta_generator = DeltaGenerator(ReportQueue())
        # TODO(armando): Figure out how to get code coverage on this.
        # Module imports are hard to mock and cover ie
        # streamlit.__init__.py vs streamlit.some_file.py  We test the
        # functionality of DeltaConnection in delta_connection_test.py
        # so right now getting code coverage on this decorator isn't
        # that critical.
        #
        # Only output if the config allows us to.
        elif config.get_option('client.displayEnabled'):  # pragma: no cover
            connection = DeltaConnection.get_connection()
            delta_generator = connection.get_delta_generator()
        else:  # pragma: no cover
            delta_generator = _NULL_DELTA_GENERATOR

        return method(delta_generator, *args, **kwargs)
    return wrapped_method


# DeltaGenerator methods:

altair_chart    = _with_dg(DeltaGenerator.altair_chart)  # noqa: E221
area_chart      = _with_dg(DeltaGenerator.area_chart)  # noqa: E221
audio           = _with_dg(DeltaGenerator.audio)  # noqa: E221
balloons        = _with_dg(DeltaGenerator.balloons)  # noqa: E221
bar_chart       = _with_dg(DeltaGenerator.bar_chart)  # noqa: E221
bokeh_chart     = _with_dg(DeltaGenerator.bokeh_chart)  # noqa: E221
code            = _with_dg(DeltaGenerator.code)  # noqa: E221
dataframe       = _with_dg(DeltaGenerator.dataframe)  # noqa: E221
deck_gl_chart   = _with_dg(DeltaGenerator.deck_gl_chart)  # noqa: E221
empty           = _with_dg(DeltaGenerator.empty)  # noqa: E221
error           = _with_dg(DeltaGenerator.error)  # noqa: E221
exception       = _with_dg(DeltaGenerator.exception)  # noqa: E221
header          = _with_dg(DeltaGenerator.header)  # noqa: E221
help            = _with_dg(DeltaGenerator.help)  # noqa: E221
image           = _with_dg(DeltaGenerator.image)  # noqa: E221
info            = _with_dg(DeltaGenerator.info)  # noqa: E221
json            = _with_dg(DeltaGenerator.json)  # noqa: E221
line_chart      = _with_dg(DeltaGenerator.line_chart)  # noqa: E221
map             = _with_dg(DeltaGenerator.map)  # noqa: E221
markdown        = _with_dg(DeltaGenerator.markdown)  # noqa: E221
plotly_chart    = _with_dg(DeltaGenerator.plotly_chart)  # noqa: E221
progress        = _with_dg(DeltaGenerator.progress)  # noqa: E221
pyplot          = _with_dg(DeltaGenerator.pyplot)  # noqa: E221
subheader       = _with_dg(DeltaGenerator.subheader)  # noqa: E221
success         = _with_dg(DeltaGenerator.success)  # noqa: E221
table           = _with_dg(DeltaGenerator.table)  # noqa: E221
text            = _with_dg(DeltaGenerator.text)  # noqa: E221
title           = _with_dg(DeltaGenerator.title)  # noqa: E221
vega_lite_chart = _with_dg(DeltaGenerator.vega_lite_chart)  # noqa: E221
video           = _with_dg(DeltaGenerator.video)  # noqa: E221
warning         = _with_dg(DeltaGenerator.warning)  # noqa: E221

_native_chart   = _with_dg(DeltaGenerator._native_chart)  # noqa: E221
_text_exception = _with_dg(DeltaGenerator._text_exception)  # noqa: E221

# Config
set_option = config.set_option
get_option = config.get_option

# Special methods:

def write(*args):
    """Write arguments to the report.

    This is the swiss-army knife of Streamlit commands. It does different
    things depending on what you throw at it.

    Unlike other Streamlit commands, write() has some unique properties:

        1. You can pass in multiple arguments, all of which will be written.
        2. Its behavior depends on the input types as follows.
        3. It returns None, so it's "slot" in the report cannot be reused.

    Parameters
    ----------
    *args : any
        One or many objects to print to the Report.

    Arguments are handled as follows:

        - write(string)     : Prints the formatted Markdown string.
        - write(data_frame) : Displays the DataFrame as a table.
        - write(error)      : Prints an exception specially.
        - write(func)       : Displays information about a function.
        - write(module)     : Displays information about the module.
        - write(dict)       : Displays dict in an interactive widget.
        - write(obj)        : The default is to print str(obj).
        - write(mpl_fig)    : Displays a Matplotlib figure.
        - write(altair)     : Displays an Altair chart.
        - write(plotly_fig) : Displays a Plotly figure.
        - write(bokeh_fig)  : Displays a Bokeh figure.

    Example
    -------

    Its simplest use case is to draw Markdown-formatted text, whenever the
    input is a string:

    >>> write('Hello, *World!*')

    .. output::
       https://share.streamlit.io/0.25.0-2JkNY/index.html?id=DUJaq97ZQGiVAFi6YvnihF
       height: 50px

    As mentioned earlier, `st.write()` also accepts other data formats, such as
    numbers, data frames, styled data frames, and assorted objects:

    >>> st.write(1234)
    >>> st.write(pd.DataFrame({
    ...     'first column': [1, 2, 3, 4],
    ...     'second column': [10, 20, 30, 40],
    ... }))

    .. output::
       https://share.streamlit.io/0.25.0-2JkNY/index.html?id=FCp9AMJHwHRsWSiqMgUZGD
       height: 250px

    Finally, you can pass in multiple arguments to do things like:

    >>> st.write('1 + 1 = ', 2)
    >>> st.write('Below is a DataFrame:', data_frame, 'Above is a dataframe.')

    .. output::
       https://share.streamlit.io/0.25.0-2JkNY/index.html?id=DHkcU72sxYcGarkFbf4kK1
       height: 300px

    Oh, one more thing: `st.write` accepts chart objects too! For example:

    >>> import pandas as pd
    >>> import numpy as np
    >>> import altair as alt
    >>>
    >>> df = pd.DataFrame(
    ...     np.random.randn(200, 3),
    ...     columns=['a', 'b', 'c'])
    ...
    >>> c = alt.Chart(df).mark_circle().encode(
    ...     x='a', y='b', size='c', color='c')
    >>>
    >>> st.write(c)

    .. output::
       https://share.streamlit.io/0.25.0-2JkNY/index.html?id=8jmmXR8iKoZGV4kXaKGYV5
       height: 200px

    """
    HELP_TYPES = (
        types.FunctionType,
        types.ModuleType,
    )

    try:
        string_buffer = []

        def flush_buffer():
            if string_buffer:
                markdown(' '.join(string_buffer))  # noqa: F821
                string_buffer[:] = []

        for arg in args:
            if isinstance(arg, string_types):  # noqa: F821
                string_buffer.append(arg)
            elif type(arg).__name__ in _DATAFRAME_LIKE_TYPES:
                flush_buffer()
                dataframe(arg)  # noqa: F821
            elif isinstance(arg, Exception):
                flush_buffer()
                exception(arg)  # noqa: F821
            elif isinstance(arg, HELP_TYPES):
                flush_buffer()
                help(arg)
            elif util.is_altair_chart(arg):
                flush_buffer()
                altair_chart(arg)
            elif util.is_type(arg, 'matplotlib.figure.Figure'):
                flush_buffer()
                pyplot(arg)
            elif util.is_plotly_chart(arg):
                flush_buffer()
                plotly_chart(arg)
            elif util.is_type(arg, 'bokeh.plotting.figure.Figure'):
                flush_buffer()
                bokeh_chart(arg)
            elif type(arg) in dict_types:
                flush_buffer()
                json(arg)
            else:
                string_buffer.append('`%s`' % util.escape_markdown(str(arg)))

        flush_buffer()

    except Exception:
        _, exc, exc_tb = sys.exc_info()
        exception(exc, exc_tb)  # noqa: F821


@contextlib.contextmanager
def spinner(text='In progress...'):
    """Temporarily displays a message while executing a block of code.

    Parameters
    ----------
    text : str
        A message to display while executing that block

    Example
    -------

    >>> with st.spinner('Wait for it...'):
    >>>     time.sleep(5)
    >>> st.success('Done!')

    """
    try:
        # Set the message 0.1 seconds in the future to avoid annoying
        # flickering if this spinner runs too quickly.
        DELAY_SECS = 0.1
        message = empty()  # noqa: F821
        display_message = True
        display_message_lock = threading.Lock()

        def set_message():
            with display_message_lock:
                if display_message:
                    message.warning(str(text))

        threading.Timer(DELAY_SECS, set_message).start()

        # Yield control back to the context.
        yield
    finally:
        with display_message_lock:
            display_message = False
        message.empty()


@contextlib.contextmanager
def echo():
    """Use in a `with` block to draw some code on the report, then execute it.

    Example
    -------

    >>> with st.echo():
    >>>     st.write('This code will be printed')

    """
    from streamlit.compatibility import running_py3
    code = empty()  # noqa: F821
    try:
        spaces = re.compile('\s*')
        frame = traceback.extract_stack()[-3]
        if running_py3():
            filename, start_line = frame.filename, frame.lineno
        else:
            filename, start_line = frame[:2]
        yield
        if running_py3():
            end_line = traceback.extract_stack()[-3].lineno
        else:
            end_line = traceback.extract_stack()[-3][1]
        lines_to_display = []
        with open(filename) as source_file:
            source_lines = source_file.readlines()
            lines_to_display.extend(source_lines[start_line:end_line])
            initial_spaces = spaces.match(lines_to_display[0]).end()
            for line in source_lines[end_line:]:
                if spaces.match(line).end() < initial_spaces:
                    break
                lines_to_display.append(line)
        lines_to_display = textwrap.dedent(''.join(lines_to_display))
        code.code(lines_to_display, 'python')

    except FileNotFoundError as err:  # noqa: F821
        code.warning('Unable to display code. %s' % err)
