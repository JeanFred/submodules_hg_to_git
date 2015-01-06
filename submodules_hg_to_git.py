import os.path
import sys


class HgSub:

    def __init__(self, repo):
        self.repo = repo
        self.sub = {}
        self.substate = {}

    @staticmethod
    def parse_hgsub_file(file_handle):
        for line in file_handle:
            try:
                (name, url) = line.split('=')
                yield (name.strip(), url.strip())
            except ValueError, e:
                print line

    @staticmethod
    def parse_hgsubstate_file(file_handle):
        for line in file_handle:
            (commit, name) = line.split(' ')
            yield (name.strip(), commit.strip())

    def parse_hg_repo(self):
        hgsub_file = os.path.join(self.repo, '.hgsub')
        self.sub = self.hgsub_file_to_dict(hgsub_file)
        hgsubstate_file = os.path.join(self.repo, '.hgsubstate')
        self.substate = self.hgsubstate_file_to_dict(hgsubstate_file)

    def hgsub_file_to_dict(self, hgsub_file):
        with open(hgsub_file, 'r') as f:
            return dict(list(self.parse_hgsub_file(f)))

    def hgsubstate_file_to_dict(self, hgsubstate_file):
        with open(hgsubstate_file, 'r') as f:
            return dict(list(self.parse_hgsubstate_file(f)))

    def repo_to_commands(self):
        self.parse_hg_repo()
        for directory, repo_url in self.sub.items():
            commit = self.substate[directory]
            if repo_url.startswith('[git]'):
                repo_url = repo_url[5:]
                yield self.make_shell_commands(repo_url, directory, commit)
            else:
                pass

    def make_shell_commands(self, repo_url, directory, commit):
        return [
            self.make_submodule_shell_command(repo_url, directory),
            self.make_change_directory_shell_commands(directory),
            self.make_branch_shell_command(commit),
            'cd ..'
        ]

    @staticmethod
    def make_submodule_shell_command(repo_url, directory):
        command = 'git submodule add %s %s'
        return command % (repo_url, directory)

    @staticmethod
    def make_change_directory_shell_commands(directory):
        command = 'cd %s'
        return command % directory

    @staticmethod
    def make_branch_shell_command(commit):
        command = 'git checkout -b %s %s'
        return command % (commit, commit)

    def convert_repo(self):
        for commands in self.repo_to_commands():
            yield '\n'.join(commands)


def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = '.'
    obj = HgSub(directory)
    print '\n'.join(obj.convert_repo())


if __name__ == "__main__":
    main()
