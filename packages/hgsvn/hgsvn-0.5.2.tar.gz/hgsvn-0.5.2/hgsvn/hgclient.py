from hgsvn import ui
from hgsvn.ui import (is_debug
                     , encode, encodes
                     )
from hgsvn.errors import ExternalCommandFailed, HgSVNError, RunCommandError
from hgsvn.shell import (locale_encoding
    , run_args
    )

import os
import hglib
from hglib import util
from hglib.util import b
import six
from six import binary_type, text_type, print_
import codecs

hgseance = None		#hgclient
# this path where seance run from
hgseance_cwd = None

def run_hg(args=None, bulk_args=None, output_is_locale_encoding=False, prompt = None):
    """
    Run a Mercurial command, returns the (unicode) output.
    bulk_args - are filenames ordinary. it is encoded to locale_encoding for hglib
    """

    def decode_output(output, enc):
        # some hg cmds, for example "log" return output with mixed encoded lines, therefore decode them 
        # line by line independently
        #outlines = output #.splitlines(True)
        try:
            outlines = output.encode(enc, errors = 'strict').splitlines(True) #'utf-8'
        except:
            binlines = output.splitlines(True);
            hgcodec = codecs.lookup(enc)
            loccodec = codecs.lookup(locale_encoding)
            outlines = list();
            for line in binlines:
                try:
                    #uline = unicode(line, encoding='utf-8', errors = 'ignore')
                    uline, ulen = hgcodec.decode(line, errors='strict')#encoding or locale_encoding or 'UTF-8'
                except UnicodeDecodeError:
                    uline, ulen = loccodec.decode(line, errors='strict')#encoding or locale_encoding or 'UTF-8'
                    if ui._level >= ui.PARSE:
                        print_(locale_encoding, ":", line)
                    #uline = unicode(line, encoding=locale_encoding, errors = 'ignore')
                outlines.append(uline)
            
        if ui._level >= ui.PARSE:
            print_(outlines)
        res = ''
        for line in outlines:
            if ui._level >= ui.PARSE:
                print_(encode(line, locale_encoding))
            res += line
            #try:
            #    res += line.decode(enc, errors='ignore')#encoding or locale_encoding or 'UTF-8'
            #except UnicodeDecodeError:
            #    res += line.decode(locale_encoding, errors='ignore')#encoding or locale_encoding or 'UTF-8'
        return res
    
    pass_args = None
    def prepare_args(args, target_encode):
        return encodes(args, target_encode)

    global hgseance
    global hgseance_cwd
    enc = locale_encoding; #'utf-8'; #
        
    def invoke_cmd_by_hgseance(hgargs, fail_if_stderr=False):
        global hgseance
        try:
            hgenc = hgseance.encoding.decode()
            hgcodec = codecs.lookup(hgenc)
            args = hgargs
            for i in range(len(args)):
                s = hgargs[i]
                if isinstance(s, text_type):
                    ui.status("hg: take param %s as text"%(s), level=ui.TRACECMD)
                    s,slen = hgcodec.encode(s)
                    args[i] = s
        
            ui.status("* hg %s"%args, level=ui.DEBUG)
            pass_args = tuple(args)
            out = hgseance.rawcommand(args, prompt = prompt)
            return decode_output(out, enc)
        except (hglib.error.CommandError) as e:
            if tuple(e.args) == pass_args:
                raise RunCommandError("External program failed", e.ret, hgargs, e.err, e.out, codec = hgcodec)
            else:
                if args[0]=='heads':
                    ui.status("*hg try again %s"%args, level = ui.WARNING)
                    try:
                        out = hgseance.rawcommand(pass_args, prompt = prompt)
                        return decode_output(out, enc)
                    except (hglib.error.CommandError) as e:
                        if e.args == pass_args:
                            raise RunCommandError("External program sure failed", e.ret, hgargs, e.err, e.out, codec = hgcodec)
                        else:
                            raise RunCommandError("External program failed on strange args", e.ret, e.args, e.err, e.out, codec = hgcodec)
                else:
                    ui.status("passed args:%s\nreturned args:%s"%(pass_args, e.args), level=ui.DEBUG)
                    raise RunCommandError("External program failed on strange args", e.ret, e.args, e.err, e.out, codec = hgcodec)

    if not (hgseance is None):
        # if run from other cwd, need reconnect new hg seance to work in current cwd
        if hgseance_cwd != os.getcwd():
            hg_close()

    if hgseance is None:
        hgseance = hglib.open(path='.', encoding='utf-8')
        hgseance_cwd = os.getcwd()
        ui.status("opened hg seance with encoding %s"%hgseance.encoding, level=ui.DEBUG)

    enc = hgseance.encoding.decode()
    
    try:
        output = run_args(invoke_cmd_by_hgseance, args, prepare_args(bulk_args, locale_encoding), encoding=locale_encoding)
    except :
        #on any exception destroy and recreate new hgseance for next commands
        del hgseance
        hgseance = None
        raise
    return output

def hg_close():
    global hgseance
    if hgseance is None:
        return
    hgseance.close()
    del hgseance
    hgseance = None
    hgseance_cwd = None

def hg_init():
	#import pdb; pdb.set_trace()
    hgseance = hglib.init(dest='.', encoding=u'utf-8')
    del hgseance

def hg_invoke(args):
    from hglib import HGPATH, error

    cmd = [hglib.HGPATH]+args

    proc = hglib.util.popen(cmd)
    out, err = proc.communicate()

    if proc.returncode:
        raise error.CommandError(args, proc.returncode, out, err)

    enc = locale_encoding #'utf-8'; #
    hgcodec = codecs.lookup(enc)
    outline, length = hgcodec.decode(out)
    return outline
