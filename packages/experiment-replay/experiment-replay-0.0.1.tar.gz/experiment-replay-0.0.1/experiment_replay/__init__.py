import git
import subprocess
import datetime
import sys
import random

PREFIX = "ExpReplay"
#  Prepare to escape in amend_command
COMMIT_LINE = 'ExpReplay: {id} \\"{command}\\" {date}'


def setup():
    repo = git.Repo(search_parent_directories=True)
    if repo.is_dirty():
        raise Exception("Repo is dirty")
    if len(repo.untracked_files) != 0:
        raise Exception("You have some untracked files, stash or commit to continue")
    sha = repo.head.object.hexsha
    command = " ".join(["python"] + sys.argv)
    id = "%06x" % random.getrandbits(24)
    line = COMMIT_LINE.format(id=id, command=command, date=datetime.datetime.now())

    amend_command = f"""GIT_EDITOR="echo '{line}' >> $1" git commit --amend"""
    subprocess.call(amend_command, shell=True)
    return sha
