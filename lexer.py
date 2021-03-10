import sys
import SCANNER

from enum import Enum
class Status(Enum):
    ALIVE = 0
    DEAD = 1

def read_def(def_file):
    lines = []
    try:
        with open(def_file, "r") as f:
            lines = f.readlines()
        if len(lines) == 0:
            print("Error: File is empty.", file=sys.stderr)
            exit(1)
    except IOError:
        print("Error: Def file does not appear to exist.", file=sys.stderr)
        exit(1)

    return lines

def extract_chars(char_line):
    characters = []
    i = 0
    char_line = char_line.strip()
    char_line = char_line.replace(" ", "")
    while i < len(char_line):
        current = char_line[i]
        if current == "x":
            current += char_line[i+1:i+3]
            current = current.lower()
            i += 3
        else:
            current = char_to_alphabet(current)
            i += 1
        characters.append(current)
    
    return characters

def scan_def(definition, parent_folder):
    characters = extract_chars(definition[0])
    scanners = set()
    for line in definition[1:]:
        line = line.strip().split()
        temp = SCANNER.SCANNER(*line[1:])
        temp.initialize(parent_folder + "/" + line[0], characters)
        scanners.add(temp)
    
    return scanners

def read_source(source_file):
    data = None
    line_sizes = []
    try:
        with open(source_file, "r") as f:
            data = f.read()
            f.seek(0)
            lines = f.readlines()
            line_sizes = [len(x) for x in lines]
        if len(data) == 0:
            print("Error: File is empty.", file=sys.stderr)
            exit(0)
    except IOError:
        print("Error: Source file does not appear to exist.", file=sys.stderr)
        exit(1)
    
    return data, line_sizes

def char_to_alphabet(char):
    return "x{:02x}".format(ord(char))

def string_to_alphabet(string):
    return_string = ""
    for char in string:
        if char.isalpha() or char.isdigit() and char != "x":
            return_string += char
        else:
            return_string += char_to_alphabet(char)
    
    return return_string

def get_line_col_from_idx(index, line_sizes):
    line, col = 0, 0
    for line_size in line_sizes:
        if index < line_size:
            col = index
            break
        else:
            index -= line_size
            line += 1
    
    return line + 1, col + 1

def results_to_file(results, source, line_sizes, file):
    try:
        with open(file, "w") as f:
            for result in results:
                line, col = get_line_col_from_idx(result[1][0], line_sizes)
                if result[0].value is None:
                    print(f"{result[0].id} {string_to_alphabet(source[result[1][0]:result[1][1]])} {line} {col}", file=f)
                else:
                    print(f"{result[0].id} {string_to_alphabet(result[0].value)} {line} {col}", file=f)
    except IOError:
        print("Error: File does not appear to exist.", file=sys.stderr)
        exit(1)

def find_tokens(scanners, source):
    matched = dict.fromkeys(scanners, None)
    results = []
    index = 0
    while index < len(source):
        matched.clear()
        for scanner in scanners:
            temp = 0
            state = 0
            while temp + index < len(source):
                temp_char = source[index + temp]
                char = char_to_alphabet(temp_char)
                if scanner.dfa[state, char] != "E":
                    state = int(scanner.dfa[state, char])
                    temp += 1
                else:
                    break
                if int(state) in scanner.dfa.acc_states:
                    matched[scanner] = (index, index + temp)

        best_scanner = None
        longest_match = None
        for scanner in matched:
            if longest_match is None:
                best_scanner = scanner
                longest_match = matched[scanner]
            elif matched[scanner][1] > longest_match[1]:
                best_scanner = scanner
                longest_match = matched[scanner]
            elif (matched[scanner][1] == longest_match[1] and scanner.prority < best_scanner.prority):
                best_scanner = scanner
                longest_match = matched[scanner]

        results.append((best_scanner, longest_match))
        index = longest_match[1]
    
    return results

def lexer(def_file, source_file, out_file):
    definition = read_def(def_file)
    parent_folder = def_file.split("/")[0]
    source, line_sizes = read_source(source_file)
    scanners = scan_def(definition, parent_folder)
    results = find_tokens(scanners, source)
    results_to_file(results, source, line_sizes, out_file)

if __name__ == "__main__":
    lexer("_luthertest/tied/a/scan.u", "_luthertest/tied/a/program.src", "./_output.tok")