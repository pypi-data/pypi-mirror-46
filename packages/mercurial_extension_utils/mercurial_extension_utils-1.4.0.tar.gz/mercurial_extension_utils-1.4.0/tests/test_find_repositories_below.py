
import mercurial_extension_utils as meu
import os
import tempfile
import shutil
import subprocess
import unittest


class RepoBuffer(object):
    def __init__(self):
        self.location = tempfile.mkdtemp()
        self.setup_repos()

    def __del__(self):
        shutil.rmtree(self.location)

    def setup_repos(self):
        self._exec_in_top("hg", "init", "c/c1/c11-repo")
        self._exec_in_top("hg", "init", "a-repo")
        self._exec_in_top("hg", "init", "b/b3/b3a-repo")
        self._exec_in_top("hg", "init", "b/b1-repo")
        self._exec_in_top("hg", "init", "b/b2-repo")
        self._exec_in_top("hg", "init", "b/b3/b3b-repo")
        self._exec_in_top("hg", "init", "a-repo/a1-subrepo")
        self._exec_in_top("hg", "init", "b/b1-repo/b11-subrepo")

    def _exec_in_top(self, *args):
        status = subprocess.Popen(args, cwd=self.location).wait()
        if status:
            raise subprocess.CalledProcessError(status, args[0])


class TestFindRepositories(unittest.TestCase):

    buffer = RepoBuffer()

    def _check_path_and_fix(self, repo_path, where):
        self.assertTrue(os.path.isdir(repo_path))
        self.assertTrue(os.path.isabs(repo_path))
        self.assertTrue(os.path.isdir(os.path.join(repo_path, ".hg")))
        norm_where = meu.normalize_path(where)
        fixed_path = repo_path.replace(norm_where, "/xxx")
        if fixed_path == repo_path:
            self.fail("Failed to normalize path, repo_path %s, where %s" % (repo_path, norm_where))
        return fixed_path

    def test_std(self):
        where = self.buffer.location
        items = []
        for repo_path in meu.find_repositories_below(where):
            items.append(self._check_path_and_fix(repo_path, where))
        self.assertEqual(items, [
            "/xxx/a-repo",
            "/xxx/b/b1-repo",
            "/xxx/b/b2-repo",
            "/xxx/b/b3/b3a-repo",
            "/xxx/b/b3/b3b-repo",
            "/xxx/c/c1/c11-repo",
        ])

    def test_std_check_inside(self):
        where = self.buffer.location
        items = []
        for repo_path in meu.find_repositories_below(where, check_inside=True):
            items.append(self._check_path_and_fix(repo_path, where))
        self.assertEqual(items, [
            "/xxx/a-repo",
            "/xxx/a-repo/a1-subrepo",
            "/xxx/b/b1-repo",
            "/xxx/b/b1-repo/b11-subrepo",
            "/xxx/b/b2-repo",
            "/xxx/b/b3/b3a-repo",
            "/xxx/b/b3/b3b-repo",
            "/xxx/c/c1/c11-repo",
        ])

    def test_from_repo(self):
        where = self.buffer.location
        items = []
        for repo_path in meu.find_repositories_below(
                os.path.join(where, "a-repo")):
            items.append(self._check_path_and_fix(repo_path, where))
        self.assertEqual(items, [
            "/xxx/a-repo",
        ])

    def test_from_repo_check_inside(self): 
        where = self.buffer.location
        items = []
        for repo_path in meu.find_repositories_below(
                os.path.join(where, "a-repo"), check_inside=True):
            items.append(self._check_path_and_fix(repo_path, where))
        self.assertEqual(items, [
            "/xxx/a-repo",
            "/xxx/a-repo/a1-subrepo",
        ])


if __name__ == "__main__":
    unittest.main()
