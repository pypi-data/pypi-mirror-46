# coding=utf-8

import locale
import os
import shutil
import subprocess
import tempfile
import unittest
import six

#from hgsvn import common
from hgsvn import ui
from hgsvn import common
from hgsvn.shell import find_program
from hgsvn.run import hgpushsvn
from hgsvn.hgclient import hg_close, run_hg

from six import *
from nose import SkipTest
from nose.tools import *

#ui.verbose_level(ui.TRACECMD)#PARSEINNER
#ui.verbose_level(ui.PARSEINNER)
ui._UseTerminalWidth = 256

class RepoTest(unittest.TestCase):

    def _run_cmd(self, cmd_args):
        useargs = cmd_args
        useargs[0] = find_program(cmd_args[0])
        ui.status("run: %s"%(cmd_args), level = ui.DEBUG);
        p = subprocess.Popen(useargs)
        p.wait()
        del p

    def _write_file(self, fname, content, commit=False, added=False,
                    msg='test'):
        f = open(os.path.join(self.repo_dir, fname), 'w')
        f.write(content)
        f.close()
        if added:
            self._run_cmd(['hg', 'add', fname])
        if commit:
            self._run_cmd(['hg', 'commit', '-m', msg])

    def _remove_file(self, fname, commit=False):
        self._run_cmd(['hg', 'rm', fname])
        if commit:
            self._run_cmd(['hg', 'commit', '-m', 'test'])

    def _move_file(self, source, dest, commit=False):
        self._run_cmd(['hg', 'mv', source, dest])
        if commit:
            self._run_cmd(['hg', 'commit', '-m',
                           '"Copied %s -> %s"' % (source, dest)])

    def setUp(self):
        #ui.verbose_level(ui.TRACECMD)
        self.repo_dir = tempfile.mkdtemp()
        self._currdir = os.getcwd()
        os.chdir(self.repo_dir)
        self._run_cmd(['hg', 'init'])
        self.test_file = os.path.join(self.repo_dir, 'foo')
        f = open(self.test_file, 'w')
        f.write('foo')
        f.close()
        self._run_cmd(['hg', 'add', 'foo'])
        self._run_cmd(['hg', 'commit', '-m', '"Initial."'])
        ui.status("have test setup at %s"%self.repo_dir, level = ui.DEBUG);
        #sumary - 
        #   tip: Added foo

    def tearDown(self):
        #ui.verbose_level(ui.DEFAULT)
        os.chdir(self._currdir)
        hg_close()
        try:
            shutil.rmtree(self.repo_dir)
        except:
            print("warning!!! some locks leaves of dir %s"%self.repo_dir)
