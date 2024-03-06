from sys import argv
from os import path

usage = '''Usage: <python> Snitkin_hw1.py <in.file.txt>

    <python> - your Python version (Python 2 and 3 compatible)
    Snitkin_hw1.py - this Python script name
    <in.file.txt> - input file with your data
    
The input file should contain at least two lines for two sequences to be aligned.
Additionally, you may provide more lines:
line 3 - score for match ('default' is for default value: 1)
line 4 - score for mismatch ('default' is for default value: 0)
line 5 - penalty for gap ('default' is for default value: -1)
line 6 - boolean defining if matching pattern is needed in output ('true', '1')
or not ('false', '0')

Output:
line 1 - alignment score
lines 2 and 3 - alignment itself
'''

if len(argv) < 2:
    print('\nWARNING! No input file provided!\n')
    print(usage)
    exit()

if argv[1] in ['--help', '-h']:
    print(usage)
    exit()

if not path.isfile(argv[1]):
    print('\nWARNING! Input file not found:', argv[1])
    print()
    print(usage)
    exit()

input_file = open(argv[1], 'r')
input_data = input_file.read().strip().split('\n')
input_file.close()

if len(input_data) < 2:
    print('\nWARNING! Not enough data in the input file!\n')
    print(usage)
    exit()

if len(input_data) > 2:
    for i in range(2, min(5, len(input_data))):
        data_stripped = u"{}".format(input_data[i].lstrip('-'))
        if not data_stripped.isnumeric() and data_stripped != 'default':
            print('\nWARNING! Scoring data should be numeric!')
            print('`{}` is given on line {}.\n'.format(input_data[i], i+1))
            print(usage)
            exit()

seq1 = input_data[0].strip()
seq2 = input_data[1].strip()
match = int(float(input_data[2])) if len(input_data) > 2 and input_data[2] != 'default' else 1
mismatch = int(float(input_data[3])) if len(input_data) > 3 and input_data[3] != 'default' else 0
gap = int(float(input_data[4])) if len(input_data) > 4 and input_data[4] != 'default' else -1

# Create empty matrix
matrix = []
for _ in range(len(seq1) + 1):
    matrix.append([0] * (len(seq2) + 1))

# Fill the first row and column with penalties for gaps
for i in range(1, len(matrix)):
    matrix[i][0] = matrix[i - 1][0] + gap
for j in range(1, len(matrix[0])):
    matrix[0][j] = matrix[0][j - 1] + gap

# Counting scores in the rest of the matrix
for i in range(1, len(matrix)):
    for j in range(1, len(matrix[i])):
        letter1 = seq1[i - 1]
        letter2 = seq2[j - 1]
        score = match if letter1 == letter2 else mismatch
        score = max(matrix[i][j - 1] + gap,
                    matrix[i - 1][j] + gap,
                    matrix[i - 1][j - 1] + score
                    )
        matrix[i][j] = score

align1 = ''
align2 = ''
i = len(seq1)
j = len(seq2)
total_score = 0

# Reverse passage through matrix, alignment reconstruction, counting score
while i > 0 or j > 0:
    letter1 = seq1[i - 1]
    letter2 = seq2[j - 1]
    score = match if letter1 == letter2 else mismatch
    if i > 0 and j > 0 and matrix[i][j] == matrix[i - 1][j - 1] + score:
        align1 = letter1 + align1
        align2 = letter2 + align2
        i -= 1
        j -= 1
        total_score += score
    elif matrix[i][j] == matrix[i - 1][j] + gap:
        align1 = letter1 + align1
        align2 = '-' + align2
        i -= 1
        total_score -= 1
    else:
        align1 = '-' + align1
        align2 = letter2 + align2
        j -= 1
        total_score -= 1

# Print output
print(total_score)
print(align1)

# Print matching pattern
if len(input_data) > 5 and input_data[5] in ['true', '1']:
    match_pattern = ''
    for i in range(len(align1)):
        match_pattern += '|' if align1[i] == align2[i] else ' '
    print(match_pattern)

print(align2)
