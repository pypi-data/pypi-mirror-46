from hgsvn import ui
from hgsvn.ui import is_debug, encode, encodes, decode, decodes
from hgsvn.errors import ExternalCommandFailed, HgSVNError, RunCommandError

import os
import locale
from datetime import datetime
import time
from subprocess import Popen, PIPE, STDOUT
import shutil
import stat
import sys
import traceback
import codecs
import fileinput
import re
import hglib
import six
import codecs

from six import string_types, binary_type, text_type, b

def c_style_unescape(string):
    if string[0] == string[-1] == '"':
        return string.decode('string-escape')[1:-1]
    return string

# Windows compatibility code by Bill Baxter
if os.name == "nt":
    def find_program(name):
        """
        Find the name of the program for Popen.
        Windows is finnicky about having the complete file name. Popen
        won't search the %PATH% for you automatically.
        (Adapted from ctypes.find_library)
        """
        if os.path.exists(name):
            return name

        # See MSDN for the REAL search order.
        base, ext = os.path.splitext(name)
        if ext:
            exts = [ext]
        else:
            exts = ['.bat', '.exe']
        for directory in os.environ['PATH'].split(os.pathsep):
            if len(directory) <= 1:
                continue
            directory = c_style_unescape(directory)
            for e in exts:
                fname = os.path.join(directory, base + e)
                if os.path.exists(fname):
                    return fname
        return name
else:
    def find_program(name):
        """
        Find the name of the program for Popen.
        On Unix, popen isn't picky about having absolute paths.
        """
        return name


def _rmtree_error_handler(func, path, exc_info):
    """
    Error handler for rmtree. Helps removing the read-only protection under
    Windows (and others?).
    Adapted from http://www.proaxis.com/~darkwing/hot-backup.py
    and http://patchwork.ozlabs.org/bazaar-ng/patch?id=4243
    """
    if func in (os.remove, os.rmdir) and os.path.exists(path):
        # Change from read-only to writeable
        os.chmod(path, os.stat(path).st_mode | stat.S_IWRITE)
        func(path)
    else:
        # something else must be wrong...
        raise

def rmtree(path):
    """
    Wrapper around shutil.rmtree(), to provide more error-resistent behaviour.
    """
    return shutil.rmtree(path, False, _rmtree_error_handler)


locale_encoding = locale.getpreferredencoding()

def get_encoding():
    return locale_encoding

def _run_raw_command(cmd, args, fail_if_stderr=False):
    ui.status("* cmd:%s args:%s"%(cmd, args), level=ui.DEBUG)
    #ui.status("* %s", render_cmd_string(cmd, args), level=ui.DEBUG)

    encoding = get_encoding() or 'UTF-8'
    argcodec = codecs.lookup(encoding)

    if sys.version_info[0] >= 3:
        def _transform_args(a):
            #py3 Popen accepts str args
            #ui.status("take param %s to text enc %s"%(a, encoding), level=ui.TRACECMD)
            return a #decode( a, get_encoding() )
    else:
        def _transform_args(a):
            #py2 Popen accepts binary_str args
            ui.status("take params %s to binary enc %s"%(a, encoding), level=ui.TRACECMD)
            return encodes(a, argcodec) #a;

    try:
        pargs = [cmd] + args
        pipe = Popen( _transform_args(pargs), executable=cmd, stdout=PIPE, stderr=PIPE)
    except OSError:
        etype, value = sys.exc_info()[:2]
        raise ExternalCommandFailed(
            "Failed running external program: %s\nError: %s"
            % (render_cmd_string(cmd, args), "".join(traceback.format_exception_only(etype, value))))

    out, err = pipe.communicate()
    #if (isinstance(out, binary_type)):
    #    out = text_type(out, locale_encoding)
    #if (isinstance(err, binary_type)):
    #    err = text_type(err, locale_encoding)
    ui.status("retval:%s\nerrcode %s"%(out, err), level=ui.PARSE)

    if b"nothing changed" == binary_type(out) : #text_type(out,locale_encoding).strip(): # skip this error
        return out
    if pipe.returncode != 0 or (fail_if_stderr and err.strip()):
        raise RunCommandError("External program failed", pipe.returncode, render_cmd_string(cmd, args), err, out)

    return out

def render_cmd_string(cmd, args):
    return "%s %s" % (cmd,  " ".join( [shell_quote(x) for x in args] ) )
    
def shell_quote(s):
    if os.name == "nt":
        q = '"'
    else:
        q = "'"
    return q + s.replace('\\', '\\\\').replace("'", "'\"'\"'") + q

def getstatusoutput(cmd): 
    """Return (status, output) of executing cmd in a shell."""
    """This new implementation should work on all platforms."""
    ui.status("getstatusoutput: cmd=%s"%(cmd), level=ui.TRACECMD)
    import subprocess
    pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) #, universal_newlines=True)  
    output, sts = pipe.communicate()
    #output = "".join(pipe.stdout.readlines()) 
    #sts = pipe.returncode
    if sts is None: sts = 0
    return sts, output
    
def _run_raw_shell_command(cmd):
    ui.status("* %s"%(cmd), level=ui.DEBUG)
    st, out = getstatusoutput(cmd)
    if st != 0:
        raise RunCommandError("External program failed with non-zero return code", st, cmd, "", out)
    return out

def arg_as_str(a, argcodec, encoding):
    #assumes that args passes as utf8
    if isinstance(a, text_type):
        ui.status("take param %s as text"%(a), level=ui.TRACECMD)
        #a,alen = argcodec.encode(a)
    elif isinstance(a, binary_type): #text_type
        s,alen = argcodec.decode(a)
        ui.status("take param %s as encode %s"%(s, encoding), level=ui.TRACECMD)
        a = s
    elif not isinstance(a, str):
        ui.status("take str %s as encode %s"%(a, encoding), level=ui.TRACECMD)
        a = str(a)
    return a;

def arg_as_bin(a, argcodec, encoding):
    #assumes that args passes as utf8
    if isinstance(a, text_type):
        s,alen = argcodec.encode(a)
        ui.status("take param %s to text"%(s, encoding), level=ui.TRACECMD)
        a = s
    elif isinstance(a, binary_type): #text_type
        #s,alen = argcodec.decode(a)
        ui.status("take param %s"%(a), level=ui.TRACECMD)
    elif not isinstance(a, str):
        ui.status("take %s as binary"%(a), level=ui.TRACECMD)
        a = binary_type(a)
    return a;
    
if sys.version_info[0] >= 3:
    #py3 Popen accepts str args
    def as_shell_arg(a, argcodec, encoding):
        return arg_as_str(a, argcodec, encoding)
else:
    #py2 Popen accepts binary_str args
    def as_shell_arg(a, argcodec, encoding):
        return arg_as_bin(a, argcodec, encoding)

    
def run_args(cmd, args=None, bulk_args=None, encoding=None, fail_if_stderr=False):
    """
    Run a command without using the shell.
    encoding - just for binary strings args denotes which encode use to dislpay in debug mesage
    """
    args = args or []
    bulk_args = bulk_args or []
    encoding = encoding or locale_encoding or 'UTF-8'
    argcodec = codecs.lookup(encoding)

    def _transform_arg(a):
        #a = a.encode(encoding or locale_encoding or 'UTF-8');
        #return as_shell_arg(a, argcodec, encoding)
        return arg_as_str(a, argcodec, encoding)

    safeargs = []
    for a in args: 
        safeargs.append(_transform_arg(a))

    if not bulk_args:
        return cmd(safeargs, fail_if_stderr)
    # If one of bulk_args starts with a slash (e.g. '-foo.php'),
    # hg and svn will take this as an option. Adding '--' ends the search for
    # further options.
    for a in bulk_args:
        if a.strip()[0] == '-':
            args.append("--")
            break
    max_args_num = 254
    i = 0
    out = None
    while i < len(bulk_args):
        stop = i + max_args_num - len(args)
        sub_args = []
        for a in bulk_args[i:stop]:
            sub_args.append(_transform_arg(a))
        part = cmd(safeargs + sub_args, fail_if_stderr)
        if not out is None:
            out = out + part
        else:
            out = part
        i = stop
    return out

def run_command(cmd, args=None, bulk_args=None, encoding=None, fail_if_stderr=False):
    cmd = find_program(cmd)

    def invoke_cmd_by_raw(args, fail_if_stderr=False):
        return _run_raw_command(cmd, args, fail_if_stderr)

    return run_args(invoke_cmd_by_raw, args, bulk_args, encoding, fail_if_stderr)

def run_shell_command(cmd, args=None, bulk_args=None, encoding=None):
    """
    Run a shell command, properly quoting and encoding arguments.
    Probably only works on Un*x-like systems.
    """
    ui.status("run_shell_command: take cmd=%s args=%s bulk=%s emcoding=%s"%(cmd, args,bulk_args,encoding), level=ui.TRACECMD)
    encoding = encoding or locale_encoding or 'UTF-8'
    argcodec = codecs.lookup(encoding)

    def invoke_cmd_by_shell(args, fail_if_stderr=False):
        def _transform_arg(a):
            #Popen accepts str args
            #ui.status("take param %s to text enc %s"%(a, encoding), level=ui.TRACECMD)
            return a #decode( a, get_encoding() )
       
        escapes = set([' ', '"', "'", '&', '|','>','<', ':', ';'])

        def _quote_arg(a):
            #a = as_shell_arg(a, argcodec, encoding)
            a = arg_as_str(a, argcodec, encoding)
            if len(set(a) & escapes) > 0:
                return shell_quote(a)
            else:
                return a
        
        shell_cmd = _quote_arg(cmd)
        if args:
            args_str = " ".join(_quote_arg(a) for a in args)
            if len(args_str) > 0:
                shell_cmd += " "+args_str
        
        return _run_raw_shell_command( _transform_arg(shell_cmd) )
    
    return run_args(invoke_cmd_by_shell, args, bulk_args, encoding)

def once_or_more(desc, retry, function, *args, **kwargs):
    """Try executing the provided function at least once.

    If ``retry`` is ``True``, running the function with the given arguments
    if an ``Exception`` is raised. Otherwise, only run the function once.

    The string ``desc`` should be set to a short description of the operation.
    """
    while True:
        try:
            return function(*args, **kwargs)
        except Exception as e:
            ui.status('%s failed: %s', desc, str(e))
            if retry:
                ui.status('Trying %s again...', desc)
                continue
            else:
                raise
