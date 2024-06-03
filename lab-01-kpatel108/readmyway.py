import os

"""
    Candidates
        UI : Allow user candidate entry, and their relative popularity weighting
        Allow for candidate CSV file to be used, last,first,relative_weight, one per line.
        See random.choices - but test it before use.
"""


# Parse all names of candidates from the given file and save them into a collection for future use
def FindCandidateFiles() -> dict:
    file_names = os.listdir()
    files_content = {}

    for fn in file_names:
        if fn.startswith("candidates"):
            files_content[len(files_content)] = fn

    return files_content


# Read the name of the candidate and return in a proper format
def ReadCandidateFile(filename):
    result = []

    with open(filename,'r', encoding='utf-8') as file:
        line_num = 0
        for line in file:
            formatline = line.strip().strip('\n').split(',')
            if line_num != 0:
                print(formatline)
                result.append((formatline[0],formatline[1],formatline[2]))
            line_num += 1

    return result
