import vigo.config as config
from vigo.common import load


class Governance:
    def __init__(self):
        """Initialize a governance object."""
        self.config = load(str(config.projects))

    def groups(self):
        return [group for group in self.config if " " not in group]
