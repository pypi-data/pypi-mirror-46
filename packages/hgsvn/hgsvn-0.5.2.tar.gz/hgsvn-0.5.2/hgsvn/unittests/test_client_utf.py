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
from hgsvn import shell
from hgsvn.shell import find_program, run_command
from hgsvn.run import hgpushsvn
from hgsvn.hgclient import hg_close, run_hg
from hgsvn.svnclient import run_svn
from . import test_hgclient_base

from six import *
from nose import SkipTest
from nose.tools import *
from .test_hgclient_base import RepoTest

#ui.verbose_level(ui.TRACECMD)#PARSEINNER
#ui.verbose_level(ui.PARSEINNER)
ui._UseTerminalWidth = 256

class TestHgClientUTF(RepoTest):
    def test_hg_utf_file_stat(self):
        fname = u'файл-фу';
        self.test_file = os.path.join(self.repo_dir, fname)
        f = open(self.test_file, 'w')
        f.write('foo')
        f.close()
        res = run_hg(['st'], [fname])
        ui.status("hg st fname reported %s"%res, level=ui.DEBUG)
        res = run_hg(['st']).splitlines()
        ui.status("hg st reported %s"%res, level=ui.DEBUG)
        #self.assertEqual
        self.assertTrue(len(res) == 1)
        self.assertTrue(res[0].startswith('?'))
        self.assertTrue(res[0].endswith(fname))

class TestSVNClientUTF(unittest.TestCase):

    def setUp(self):
        self._wd = tempfile.mkdtemp()
        self._cwd = os.getcwd()
        if len(os.listdir(self._wd)) > 0:
            #shure to use empty new directory
            shutil.rmtree(self._wd)
            self._wd = tempfile.mkdtemp()
        os.chdir(self._wd)
        #ui.verbose_level(ui.TRACECMD)
        run_command("svnadmin", ['create', 'test.svn'])
        self.svn_url = 'file:///'+self._wd+'/test.svn'
        self.svn_url = self.svn_url.replace("\\","/")
        s = run_svn(['co', self.svn_url, 'test'])
        self.test_wd = self._wd+'/test'
        os.chdir(self.test_wd)
        ui.status("have setup test at %s" % os.getcwd(), level=ui.DEBUG)

    def tearDown(self):
        ui.verbose_level(ui.DEFAULT)
        hg_close()
        os.chdir(self._cwd)
        try:
            shutil.rmtree(self._wd)
        except:
            print("warning!!! some locks leaves of dir %s"%self._wd)

    def test_svng_utf_file_add(self):
        #ui.verbose_level(ui.TRACECMD)
        ui.verbose_level(ui.PARSE)
        fdb = open(self.test_wd+u'/файл-фу.txt', "w")
        fdb.write("file фу")
        fdb.close()
        s = run_svn(['add'], [u'файл-фу.txt']).splitlines()
        ui.status(s, level=ui.DEBUG)
        self.assertTrue(len(s) == 1)
        res = s[0].split()
        ui.status("splits:%s"%res, level=ui.DEBUG)
        self.assertTrue(res[0].strip() == b"A")
        fname = res[1].strip().decode(shell.get_encoding())
        self.assertTrue(fname == u'файл-фу.txt')
