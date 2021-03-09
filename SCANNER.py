import DFA

class SCANNER:
    count = 0
    def __init__(self, id, value=None):
        self.id = id
        self.value = value
        self.dfa = DFA.DFA()
        self.prority = SCANNER.count
        SCANNER.count += 1

    def initialize(self, dfa_file, ordered_chars):
        self.dfa.load_dfa(dfa_file, ordered_chars)
