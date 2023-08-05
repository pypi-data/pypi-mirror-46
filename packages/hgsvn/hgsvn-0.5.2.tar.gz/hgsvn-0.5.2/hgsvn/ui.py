# -*- coding: utf-8 -*-

"""User interface functions."""

import os
import sys
import six
import codecs
from six import binary_type, text_type, string_types

_UseTerminalWidth = -1

try:
    # First try to import the Mercurial implementation.
    import mercurial.ui
    if getattr(mercurial.ui.ui(), 'termwidth', False):
        termwidth = mercurial.ui.ui().termwidth 
    else:
        from mercurial.util import termwidth
except ImportError:
    # Fallback to local copy of Mercurial's implementation.
    def termwidth():
        if _UseTerminalWidth > 0 :
            return _UseTerminalWidth
        if 'COLUMNS' in os.environ:
            try:
                return int(os.environ['COLUMNS'])
            except ValueError:
                pass
        try:
            import termios, array, fcntl
            for dev in (sys.stdout, sys.stdin):
                try:
                    fd = dev.fileno()
                    if not os.isatty(fd):
                        continue
                    arri = fcntl.ioctl(fd, termios.TIOCGWINSZ, '\0' * 8)
                    return array.array('h', arri)[1]
                except ValueError:
                    pass
        except ImportError:
            pass
        return 80


# Log levels
ERROR = 0
ALERT   = 3
WARNING = 5
NOTE    = 10
DEFAULT = 15
VERBOSE = 20
DEBUG = 30
PARSE = 40
PARSEINNER   = 45
TRACECMD     = 50


# Configuration
_level = DEFAULT



def encode(s, name, *args, **kwargs):
    codec = codecs.lookup(name)
    rv, length = codec.encode(s, *args, **kwargs)
    #if not isinstance(rv, (str, bytes, bytearray, string_types)):
    #    raise TypeError('Not a string or byte codec')
    return rv

def decode(s, name_or_codec, *args, **kwargs):
    if (isinstance(name_or_codec, string_types)):
        codec = codecs.lookup(name_or_codec)
    else:
        codec = name_or_codec
    rv, length = codec.decode(s, *args, **kwargs)
    #if not isinstance(rv, (str, bytes, bytearray, string_types)):
    #    raise TypeError('Not a string or byte codec')
    return rv
    
def encodes(s, name_or_codec, *args, **kwargs):
    if s is None:
        return [];
    if (isinstance(name_or_codec, string_types)):
        codec = codecs.lookup(name_or_codec)
    else:
        codec = name_or_codec
    r = []
    for arg in s:
        if (isinstance(arg, text_type)):
            rv, length = codec.encode(arg, *args, **kwargs)
            r.append(rv)
        else:
            r.append(arg)
    return r

def decodes(s, name_or_codec, *args, **kwargs):
    if (isinstance(name_or_codec, string_types)):
        codec = codecs.lookup(name_or_codec)
    else:
        codec = name_or_codec
    if s is None:
        return [];
    r = []
    for arg in s:
        if (isinstance(arg, binary_type)):
            rv, length = codec.decode(arg, *args, **kwargs)
            if not isinstance(rv, (str, bytes, bytearray)):
                raise TypeError('Not a string or byte codec')
            r.append(rv)
        else:
            r.append(arg)
    return r
    
    
def status(msg, *args, **kwargs):
    """Write a status message.

    args are treated as substitutions for msg.

    The following keyword arguments are allowed:
      level    : One of DEFAULT, VERBOSE or DEBUG.
      linebreak: If True a new line is appended to msg (default: True).
      truncate : Truncate output if larger then term width (default: True).
    """
    global _level
    level = kwargs.get('level', DEFAULT)
    if level > _level:
        return
    width = termwidth()
    if args:
        msg = msg % args
    if kwargs.get('linebreak', True):
        msg = '%s%s' % (msg, os.linesep)
    if level == ERROR:
        stream = sys.stderr
    else:
        stream = sys.stdout
    if kwargs.get('truncate', True) and level != ERROR:
        add_newline = msg.endswith('\n')
        msglines = msg.splitlines()
        for no, line in enumerate(msglines):
            if len(line) > width:
                msglines[no] = line[:width-3]+"..."
        msg = os.linesep.join(msglines)
        if add_newline:
            msg = '%s%s' % (msg, os.linesep)
    #if isinstance(msg, text_type):
    #    msg = encode(msg, 'utf-8')
    
    #if (isinstance(msg, text_type)):
    #    stream.write(encode(msg, 'utf-8'))
    #else:
    #    stream.write(msg)
    stream.write(msg)
    stream.flush()


def update_config(options):
    """Update UI configuration."""
    global _level
    global _UseTerminalWidth
    _level = options.verbosity
    if options.terminalwidth > 0:
        _UseTerminalWidth = options.terminalwidth

def is_debug():
    return (_level >= DEBUG)

def verbose_level(value):
    global _level
    _level = value
