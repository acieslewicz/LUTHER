import sys

class DFA:
    def __init__(self):
        self.trans_table = []
        self.char_to_idx = {}
        self.acc_states = set()

    def load_dfa(self, file_name, ordered_chars):
        try:
            with open(file_name, "r") as dfa_file:
                dfa_def = dfa_file.readlines()

            if len(dfa_def) == 0:
                print("Error: File is empty.", file=sys.stderr)
                exit(1)
                
            for line in dfa_def:
                rules = line.split()
                if rules[0] == "+":
                    self.acc_states.add(int(rules[1]))
                self.trans_table.append(rules[2:])
            
            self.map_chars(ordered_chars)
            
        except IOError:
            print("Error: File does not appear to exist.", file=sys.stderr)
            exit(1)
        

    def map_chars(self, ordered_chars):
        self.char_to_idx.clear()
        if len(ordered_chars) != len(self.trans_table[0]):
            return 1
        index = 0
        for char in ordered_chars:
            self.char_to_idx[char] = index
            index += 1

    def __getitem__(self, index):
        state, char = index
        if char not in self.char_to_idx:
            return 'E'
        return self.trans_table[state][self.char_to_idx[char]]

if __name__ == "__main__":
    temp = DFA()
    temp.load_dfa("noto.tt", ["a","b","c","d","e","f","g","h"])
    print(temp[0, "a"])
