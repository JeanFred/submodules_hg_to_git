#!/usr/bin/env python
import unittest
import os.path
from submodules_hg_to_git import HgSub


class HgSubCommandTestCase(unittest.TestCase):

    def test_make_submodule_shell_command(self):
        """Test make_submodule_shell_command"""
        result = HgSub.make_submodule_shell_command('git://abc.git', 'abcde')
        expected = 'git submodule add git://abc.git abcde'
        self.assertEquals(result, expected)

    def test_make_change_directory_shell_command(self):
        """Test make_change_directory_shell_command"""
        result = HgSub.make_change_directory_shell_commands('abcde')
        expected = 'cd abcde'
        self.assertEquals(result, expected)

    def test_make_branch_shell_command(self):
        """Test make_branch_shell_command"""
        result = HgSub.make_branch_shell_command('abcde')
        expected = 'git checkout -b abcde abcde'
        self.assertEquals(result, expected)


class HgSubParseTestCase(unittest.TestCase):

    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        test_dir = os.path.join(root_dir, 'test_repo')
        self.hgsubstate_file = os.path.join(test_dir, '.hgsubstate')
        self.hgsub_file = os.path.join(test_dir, '.hgsub')

    def test_parse_hgsubstate_file(self):
        """Test parse_hgsubstate_file."""
        with open(self.hgsubstate_file, 'r') as f:
            result = list(HgSub.parse_hgsubstate_file(f))
        expected = [('extern/abc', '637cacb0948f575dcc250f8057517a168e616e3f'),
                    ('extern/def', '4c045c5a83042589bc4f95e5b154589848a13807')]
        self.assertEquals(result, expected)

    def test_parse_hgsub_file(self):
        """Test parse_hgsub_file."""
        with open(self.hgsub_file, 'r') as f:
            result = list(HgSub.parse_hgsub_file(f))
        expected = [
            ('extern/abc', 'ssh://hg@bitbucket.org/example/abc'),
            ('extern/def', '[git]git+ssh://git@bitbucket.org/example/def.git')
        ]
        self.assertEquals(result, expected)


class HgSubMainTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sub = {
            'extern/abc': 'ssh://hg@bitbucket.org/example/abc',
            'extern/def': '[git]git+ssh://git@bitbucket.org/example/def.git'
        }
        cls.substate = {
            'extern/abc': '637cacb0948f575dcc250f8057517a168e616e3f',
            'extern/def': '4c045c5a83042589bc4f95e5b154589848a13807'
        }

    def setUp(self):
        root_dir = os.path.dirname(os.path.realpath(__file__))
        self.directory = os.path.join(root_dir, 'test_repo')
        self.hg = HgSub(self.directory)

    def test_set_repository(self):
        self.assertEquals(self.hg.repo, self.directory)

    def test_parse_hg_repo(self):
        self.hg.parse_hg_repo()
        self.assertEquals(self.hg.sub, self.sub)
        self.assertEquals(self.hg.substate, self.substate)

    def test_make_shell_commands(self):
        result = self.hg.make_shell_commands(1, 2, 3)
        expected = [
            'git submodule add 1 2',
            'cd 2',
            'git checkout -b 3 3',
            'cd ..'
        ]
        self.assertEquals(result, expected)

    def test_repo_to_commands(self):
        result = list(self.hg.repo_to_commands())
        expected = [[
            'git submodule add git+ssh://git@bitbucket.org/example/def.git extern/def',
            'cd extern/def',
            'git checkout -b 4c045c5a83042589bc4f95e5b154589848a13807 4c045c5a83042589bc4f95e5b154589848a13807',
            'cd ..'
        ]]
        self.assertEquals(result, expected)

if __name__ == '__main__':
    unittest.main()
