#!/bin/env python
# Add two cyphertext files to each repo.

from subprocess import call
from os import getcwd, chdir
from os.path import isdir
import re
from contextlib import contextmanager
from pathlib import Path

REPO_RE = re.compile(r"gitea@git.auc-computing.nl:(.*)/(.*).git")


def extract_name(repo):
    m = REPO_RE.match(repo)
    return m.group(1)


@contextmanager
def cwd(path):
    """with cwd(path): ..."""
    current_dir = getcwd()
    chdir(path)
    try:
        yield
    finally:
        chdir(current_dir)


HERE = Path.cwd()
ASS3DIR = Path("../assignment3")
REPOS = [r.strip() for r in open("repos.txt").readlines()]

for n, repo in enumerate(REPOS):
    team = extract_name(repo)
    teamdir = ASS3DIR / team
    print("Pushing to", team)
    if not isdir(teamdir):
        with cwd(ASS3DIR):
            call(["git", "clone", repo, team])
    with cwd(ASS3DIR / team):
        call(["git", "pull"])
        for c in [1, 2]:
            src = HERE / "team{}-enc{}.txt".format(n, c)
            dest = Path("cyphertext{}.txt".format(c))
            if not dest.exists():
                call(["cp", src, dest])
                call(["git", "add", "cyphertext{}.txt".format(c)])
                call(["git", "commit", "-m", '"Add cyphertext files."'])
                call(["git", "push"])
