import shutil
from sys import exit

import vigo.config as config
from vigo import git
from vigo.common import git_is_available


def init():
    print("Initialize the vigo configuration")
    config.vigo_dir.mkdir(parents=True)
    print("Cloning openstack/governance")
    if not git.clone(config.governance_url, str(config.vigo_dir)):
        print("\nError during init.... fail to clone openstack/governance")
    print("initialization ok!")


def sync():
    print("Synchronize the vigo configuration...", end="")
    governance = config.vigo_dir / "governance"
    if not git.pull(str(governance)):
        print("\nError during update of openstack/governance")
    print("OK!")


def reset():
    print("Reset vigo configuration...", end="")
    config.vigo_dir = config.path / ".vigo"
    if not config.vigo_dir.exists():
        print("\nnothing to do...bye!")
        exit(0)
    shutil.rmtree(str(config.vigo_dir))
    print("Done!")


def execute():
    if not git_is_available():
        print("Error: git is not available and it's require by vigo")
        print("Please install git first and try to rerun vigo")
        print("Execution aborted!")
        exit(1)
    if not config.vigo_dir.exists():
        init()
    else:
        sync()
