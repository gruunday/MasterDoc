from src import collector as col, config
import unittest
from github import Github



class TestImgManip(unittest.TestCase):

    def setUp(self):
        self.g = Github(config.github_secret)
    
    def test_ls(self):
        self.repo_lst = col.lst_repos(self.g)
        self.assertEqual(type(self.repo_lst),type([]))
