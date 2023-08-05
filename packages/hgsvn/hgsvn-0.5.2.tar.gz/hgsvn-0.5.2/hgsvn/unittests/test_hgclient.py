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
from hgsvn.errors import *
from hgsvn.shell import run_command, run_shell_command
from . import test_hgclient_base

from six import *
from nose import SkipTest
from nose.tools import *
from .test_hgclient_base import RepoTest

#ui.verbose_level(ui.TRACECMD)#PARSEINNER
#ui.verbose_level(ui.PARSEINNER)
ui._UseTerminalWidth = 256


class TestHgClient(RepoTest):

    def test_get_hg_cset(self):
        ret = hgpushsvn.get_hg_cset('tip')
        self.assertTrue(isinstance(ret, string_types))  #basestring #ret.__type__ in string_types
        self.assertEqual(ret, ret.strip())
        self.assertEqual(ret.count(':'), 1)
        first, last = ret.split(':')
        self.assertTrue(first.isdigit())
        self.assertTrue(last.isalnum())

    def test_get_hg_no_cset(self):
        try:
            ret = hgpushsvn.get_hg_cset('svn.1')
            ui.status("hg reported:%s"%res, level = ui.DEBUG)
            self.assertTrue(False)
        except (RuntimeError, RunCommandError) as e:
            ui.status("hg error reported:%s"%e, level = ui.DEBUG)
            self.assertTrue(True)
        except Exception as e:
            ui.status("error reported:%s"%e, level = ui.DEBUG)
            args = ["log", "--template", '"{rev}:{node|short}"', "-r", 'svn.1']
            try:
                res = run_hg(args)
                ui.status("hglib log reported:%s"%res, level = ui.DEBUG)
                res = run_command('hg', args)
                ui.status("hg log reported:%s"%res, level = ui.DEBUG)
            except Exception as e:
                ui.status("error reported:%s"%e, level = ui.DEBUG)
            self.assertTrue(False)

    def test_strip_hg_rev(self):
        self.assertEqual(hgpushsvn.strip_hg_rev('1:2'), '1')
        self.assertEqual(hgpushsvn.strip_hg_revid('1:2'), '2')
        self.assertEqual(hgpushsvn.strip_hg_revid('1:2\n'), '2')

    def test_get_hg_changes(self):
        ret = hgpushsvn.get_hg_changes('tip', 'tip')
        self.assertTrue(isinstance(ret, tuple))
        self.assertEqual(len(ret), 4)
        added, removed, modified, copied = ret
        self.assertTrue(isinstance(added, list))
        self.assertTrue(isinstance(removed, list))
        self.assertTrue(isinstance(modified, list))
        self.assertTrue(isinstance(copied, dict))
        self.assertEqual(len(added), 1)
        self.assertEqual(len(removed), 0)
        self.assertEqual(len(modified), 0)
        self.assertEqual(len(copied), 0)
        rev1 = hgpushsvn.strip_hg_rev(hgpushsvn.get_hg_cset('tip'))
        self._write_file('foo', 'bar')
        self._write_file('bar', 'foo', commit=True, added=True)
        rev2 = hgpushsvn.strip_hg_rev(hgpushsvn.get_hg_cset('tip'))
        ret = hgpushsvn.get_hg_changes(rev1, rev2)
        self.assertTrue(isinstance(ret, tuple))
        self.assertEqual(len(ret), 4)
        added, removed, modified, copied = ret
        self.assertTrue(isinstance(added, list))
        self.assertTrue(isinstance(removed, list))
        self.assertTrue(isinstance(modified, list))
        self.assertEqual(len(added), 1)
        self.assertEqual(len(removed), 0)
        self.assertEqual(len(modified), 1)
        rev1 = rev2
        self._remove_file('bar', commit=True)
        rev2 = hgpushsvn.strip_hg_rev(hgpushsvn.get_hg_cset('tip'))
        ret = hgpushsvn.get_hg_changes(rev1, rev2)
        self.assertTrue(isinstance(ret, tuple))
        self.assertEqual(len(ret), 4)
        added, removed, modified, copied = ret
        self.assertTrue(isinstance(added, list))
        self.assertTrue(isinstance(removed, list))
        self.assertTrue(isinstance(modified, list))
        self.assertEqual(len(added), 0)
        self.assertEqual(len(removed), 1)
        self.assertEqual(len(modified), 0)

    def test_moved_file(self):
        self._move_file('foo', 'bar', commit=True)
        ret = hgpushsvn.get_hg_changes('tip', 'tip')
        self.assertTrue(isinstance(ret, tuple))
        self.assertEqual(len(ret), 4)
        added, removed, modified, copied = ret
        self.assertEqual(len(copied), 1)
        self.assertEqual(len(modified), 0)
        self.assertEqual(len(added), 0)
        self.assertEqual(len(removed), 1)

    def test_get_hg_revs(self):
        rev = hgpushsvn.strip_hg_rev(hgpushsvn.get_hg_cset('tip'))
        self._write_file('foo', 'bar', commit=True)
        rev2 = hgpushsvn.strip_hg_rev(hgpushsvn.get_hg_cset('tip'))
        revs = hgpushsvn.get_hg_revs(rev, 'default')
        self.assertTrue(isinstance(revs, list))
        self.assertEqual(len(revs), 2)
        self.assertEqual(revs[0], rev)
        self.assertEqual(revs[1], rev2)
        self._write_file('foo', 'bar2', commit=True)
        revs = hgpushsvn.get_hg_revs(rev, 'default')
        self.assertTrue(isinstance(revs, list))
        self.assertEqual(len(revs), 3)
        self.assertEqual(revs[0], rev)
        self.assertEqual(revs[1], rev2)
        # Change test file in different branch
        self._run_cmd(['hg', 'branch', 'testing'])
        self._write_file('foo', 'bar3', commit=True)
        revs = hgpushsvn.get_hg_revs(rev, 'default')
        self.assertTrue(isinstance(revs, list))
        self.assertEqual(len(revs), 3)
        self.assertEqual(revs[0], rev)
        self.assertEqual(revs[1], rev2)

    def test_get_hg_cset_description(self):
        self._write_file('foo', 'bar', commit=True, msg='123')
        rev_raw = hgpushsvn.get_hg_cset('tip')
        rev = hgpushsvn.strip_hg_rev(rev_raw)
        ret = hgpushsvn.get_hg_cset_description(rev)
        self.assertTrue(isinstance(ret, string_types))
        self.assertEqual(ret, '123')
        self._write_file('foo', 'bar', commit=True, msg=' 123\n')
        rev_raw = hgpushsvn.get_hg_cset('tip')
        rev = hgpushsvn.strip_hg_rev(rev_raw)
        ret = hgpushsvn.get_hg_cset_description(rev)
        self.assertTrue(isinstance(ret, string_types))
        self.assertEqual(ret, '123')
