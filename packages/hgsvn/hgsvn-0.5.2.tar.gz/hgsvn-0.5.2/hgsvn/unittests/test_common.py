import os
import posixpath
import shutil
import tempfile
import six

from nose import SkipTest
from nose.tools import *

from hgsvn import common, shell
from hgsvn.errors import RunCommandError
from hgsvn.shell import (run_shell_command
    , run_command
    , once_or_more
    )
from hgsvn.hgclient import run_hg, hg_close, hg_init, hg_invoke
from hgsvn.svnclient import run_svn
from hgsvn import ui
import hgsvn.run.hgimportsvn
import hgsvn.run.hgpullsvn
from hgsvn.common import drop_nested_dirs
from six import *

#ui.verbose_level(ui.TRACECMD)#PARSEINNER
#ui.verbose_level(ui.PARSEINNER)
ui._UseTerminalWidth = 256


class TestCommands(object):
    def setUp(self):
        #ui.verbose_level(ui.TRACECMD)
        pass
    
    def test_hg(self):
        #s = run_hg(['version', '-q'])
        s = hg_invoke(['version', '-q'])
        print_(s)
        ui.status("hg ack:%s"%s, level=ui.DEBUG);
        s = s.split()[0]
        eq_(s.lower(), 'mercurial')

    def test_svn(self):
        s = run_svn(['--version', '-q'])
        ui.status("svn ack:%s"%s, level=ui.DEBUG);
        eq_(s.split(b'.')[0], b'1')

class CommandsBase(object):
    cmd_shell = None
    verbose   = ui._level
    
    def run_shell(self, cmd, args=None, bulk_args=None):
        if len(self.cmd_shell) > 0:
            return self.command_func(self.cmd_shell[0], self.cmd_shell[1:]+[cmd]+args, bulk_args)
        else:
            return self.command_func(cmd, args, bulk_args)
    
    def setUp(self):
        ui.status("test cmd %s"%self.command_func.__name__)
        if os.name == "nt":
            self.cmd_shell = ['cmd.exe', '/C']
        else:
            self.cmd_shell = None
        #ui.verbose_level(ui.PARSEINNER)

    def tearDown(self):
        ui.verbose_level(self.verbose)
        
    def test_echo(self):
        #ui.verbose_level(ui.TRACECMD)
        #ui.verbose_level(ui.PARSE)
        echo_string = 'foo'
        s = self.run_shell('echo', [ echo_string ] )
        ui.status("echo reports:%s"%s);
        s = ui.decode(s, shell.locale_encoding)
        eq_(s.rstrip(), echo_string)

    # windos cmd cant strip quotes and spec symbols from parameters
    skip_escapes = (os.name == "nt")
   
    def test_echo_with_escapes(self):
        if self.skip_escapes:
            raise SkipTest #('can`t pass LineEnd in parameter by stdin')
        echo_string = 'foo & baz' #'foo \n"\' baz'
        s = self.run_shell('echo', [echo_string])
        ui.status("echo reports:%s"%s);
        s = ui.decode(s, shell.locale_encoding)
        eq_(s.rstrip(), echo_string)

    def test_bulk_args(self):
        #ui.verbose_level(ui.TRACECMD)
        #ui.verbose_level(ui.PARSE)
        sep = b('-')
        args = ['a', 'b', 'c']
        n_args = len(args)
        bulk_args = ['%d' % i for i in range(3000)]
        out = self.run_shell('echo', [sep] + args, bulk_args)
        ui.status("test_bulk_args resulted:%s"%out, level = ui.DEBUG)
        res = ui.decode(out, shell.locale_encoding)
        sub_results = res.splitlines()
        bulk_pos = 0
        for s in sub_results:
            l = s.split()
            eq_(l.pop(0).strip(), "-")
            eq_(l[:n_args], args)
            n_bulk = len(l) - n_args
            assert n_bulk < 256
            eq_(l[n_args:], bulk_args[bulk_pos:bulk_pos + n_bulk])
            bulk_pos += n_bulk
        eq_(bulk_pos, len(bulk_args))


class TestShellCommands(CommandsBase):
    command_func = staticmethod(run_shell_command)

class TestNonShellCommands(CommandsBase):
    command_func = staticmethod(run_command)


class TestLock(object):

    test_mercurial = True

    def setUp(self):
        if self.test_mercurial:
            try:
                from mercurial.lock import lock
            except ImportError:
                raise SkipTest  # mercurial not installed
        self._test_base = tempfile.mkdtemp()
        common.fixup_hgsvn_dir(self._test_base)

    def tearDown(self):
        shutil.rmtree(self._test_base)

    def test_lock_set_release(self):
        def lock_exists():
            private_dir = os.path.join(self._test_base,
                                       common.hgsvn_private_dir)
            return common.hgsvn_lock_file in os.listdir(private_dir)

        l = common.get_hgsvn_lock(self._test_base)
        lock_file = os.path.join(self._test_base, common.hgsvn_private_dir,
                                 common.hgsvn_lock_file)
        assert (lock_exists())
        l.release()
        assert (not lock_exists())

    def test_locked(self):
        l = common.get_hgsvn_lock(self._test_base)
        lHeld = False
        try:
            common.get_hgsvn_lock(self._test_base)
        except common.LockHeld :
            lHeld = True
        assert lHeld
        l.release()



class TestSimpleFileLock(TestLock):

    test_mercurial = False

    def setUp(self):
        self._real_lock = common._lock
        self._real_lock_held = common.LockHeld
        common._lock = common._SimpleFileLock
        common.LockHeld = common._LockHeld
        super(TestSimpleFileLock, self).setUp()

    def tearDown(self):
        super(TestSimpleFileLock, self).tearDown()
        common._lock = self._real_lock
        common.LockHeld = self._real_lock_held


class TestSwitchBranch(object):

    def setUp(self):
        self._wd = tempfile.mkdtemp()
        self._cwd = os.getcwd()
        if len(os.listdir(self._wd)) > 0:
            #shure to use empty new directory
            shutil.rmtree(self._wd)
            self._wd = tempfile.mkdtemp()
        os.chdir(self._wd)
        #ui.verbose_level(ui.TRACECMD)
        hg_init()
        f = open("foo", "w")
        f.write("foo")
        f.close()
        run_hg(["add", "foo"])
        run_hg(["commit", "-m", "Initial"])
        #ui.status("have setup test at %s" % os.getcwd())

    def tearDown(self):
        os.chdir(self._cwd)
        hg_close()
        try:
            shutil.rmtree(self._wd)
        except:
            print("warning!!! some locks leaves of dir %s"%self._wd)

    def test_switch_clean_repo(self):
        run_hg(["branch", "test"])
        f = open("bar", "w")
        f.write("bar")
        f.close()
        run_hg(["add", "bar"])
        run_hg(["commit", "-m", '"bar added."'])
        eq_(True, common.hg_switch_branch("test", "default"))

    def test_switch_dirty_repo(self):
        run_hg(["branch", "test"])
        f = open("bar", "w")
        f.write("bar")
        f.close()
        run_hg(["add", "bar"])
        eq_(False, common.hg_switch_branch("test", "default"))

class TestOnceOrMore(object):
    def setUp(self):
        self._counter = 0

    def increment(self, count):
        self._counter += count
        return self._counter

    def increment_until_3(self, count):
        self.increment(count)
        if self._counter < 3:
            raise Exception("Counter not high enough yet")

    def test_no_exception(self):
        foo = once_or_more("Foo", False, self.increment, 1)
        eq_(1, self._counter)
        eq_(1, foo)
        foo = once_or_more("Foo", True, self.increment, 2)
        eq_(3, self._counter)
        eq_(3, foo)

    @raises(Exception)
    def test_with_exception_no_retry(self):
        eq_(0, self._counter)
        once_or_more("Foo", False, self.increment_until_3, 1)

    def test_with_exception_retry(self):
        eq_(0, self._counter)
        once_or_more("Foo", True, self.increment_until_3, 1)
        eq_(3, self._counter)

class TestListsFunstions(object):
    def setUp(self):
        self._counter = 0
        #ui.verbose_level(ui.PARSEINNER)

    def tearDown(self):
        ui.verbose_level(ui.DEFAULT)

    def test_drop_nested_dirs(self):
        x = ['a', 'a/b', 'b', 'b/c', 'ab', 'abc', 'ab\\e']
        drops = ['ab']
        y = drop_nested_dirs(x,drops)
        ui.status("reduction of %s - %s = %s"%(x,drops,y), level = ui.DEBUG);
        eq_(set(y) , set(['a','b', 'abc']))
        
class TestPullFiles(object):

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
        ui.status("have setup test at %s" % os.getcwd(), level=ui.DEBUG)
        self.test_a = self._wd+'/test/a'
        os.chdir(self.test_wd)
        os.mkdir(self.test_a)
        fdb = open(self.test_a+'/b.txt', "w")
        fdb.write("file b")
        fdb.close()
        fdc = open(self.test_a+'/c.txt', "w")
        fdc.write("file c")
        fdc.close()
        s = run_svn(['add', 'a'])
        ui.status(s, level=ui.DEBUG)
        s = run_svn(['ci', '-m', '"initial revision"'])
        ui.status(s, level=ui.DEBUG)
        s = run_svn(['rm', 'a/b.txt'])
        ui.status(s, level=ui.DEBUG)
        s = run_svn(['cp', 'a', 'd'])
        ui.status(s, level=ui.DEBUG)
        try:
            s = run_svn(['rm', 'a'])
            ui.status(s, level=ui.DEBUG)
        except (RunCommandError) as e:
            if e.err_have("Can't move") or e.err_have("E720032") or e.err_have("Can't remove"):
                run_svn(['cleanup'])
            else:
                raise
        #print s
        #s = run_shell_command("svn", ['mv', '--parents', 'a', 'f'])
        #s = run_svn(['mv', 'a', 'f'])
        s = run_svn(['ci', '-m', '"Moving directory with deleted file"'])
        ui.status(s, level=ui.DEBUG)
        os.chdir(self._wd)
        #run_command('hgimportsvn', [svn_url, 'test.hg'])
        self.test_hg = self._wd+'/test.hg'

    def tearDown(self):
        ui.verbose_level(ui.DEFAULT)
        hg_close()
        os.chdir(self._cwd)
        try:
            shutil.rmtree(self._wd)
        except:
            print("warning!!! some locks leaves of dir %s"%self._wd)

    def test_pull_deleted_file_of_removed_dir(self):
        os.chdir(self._wd)
        import_cmd = ['hgimportsvn', self.svn_url, self.test_hg]
        if (ui._level >= ui.DEBUG):
            import_cmd.append('-v')
        hgsvn.run.hgimportsvn.main(import_cmd)
        os.chdir(self.test_hg)
        #ui.verbose_level(ui.PARSE)
        hgsvn.run.hgpullsvn.main(['hgpullsvn'])
