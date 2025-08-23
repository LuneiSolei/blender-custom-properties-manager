from .. import config

class CPMState:
    def __init__(self):
        self.debug = config.debug
        self.expand_states = {}
        self.original_draws = {}

cpm_state = CPMState()