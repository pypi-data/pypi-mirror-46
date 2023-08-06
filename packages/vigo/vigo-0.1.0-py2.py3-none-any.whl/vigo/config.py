from pathlib import Path


path = Path.home()
vigo_dir = path / ".vigo"
governance_url = "https://github.com/openstack/governance"
projects = vigo_dir / "governance" / "reference" / "projects.yaml"


class GeneralConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, debug=False, verbose=False):
        """Initialize general configuration."""
        self.debug = debug
        self.verbose = verbose
