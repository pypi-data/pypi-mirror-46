import os

from vigo.common import execute


def clone(repo, dest=None):
    cwd = os.getcwd()
    if dest:
        os.chdir(dest)

    outs, errs = execute(["git", "clone", repo])

    if cwd != os.getcwd():
        os.chdir(cwd)

    if errs:
        return False
    return True


def fetch(repo, remote="origin"):
    cwd = os.getcwd()
    os.chdir(repo)

    outs, errs = execute(["git", "fetch", remote])

    if cwd != os.getcwd():
        os.chdir(cwd)

    if errs:
        return False
    return True


def pull(repo, remote="origin"):
    cwd = os.getcwd()
    os.chdir(repo)

    outs, errs = execute(["git", "pull", remote])

    if cwd != os.getcwd():
        os.chdir(cwd)

    if errs:
        return False
    return True
