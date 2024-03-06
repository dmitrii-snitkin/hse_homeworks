# Implement Needleman–Wunsch algorithm

## Task

Write a program that implements the Needleman–Wunsch algorithm in its simplest form: +1 for a letter match, 0 for a mismatch, linear penalty –1 for each gap. Specialized modules cannot be used (in Python, the standard `sys` module will be enough to write a program).


<ins>Input:</ins> a text file with two lines for two sequences.

<ins>Output</ins> (to stdout): three lines; the first line is the alignment weight; the second and third lines are aligned sequences (with gaps) in the same order as in the input file.

Program usage:

`python needleman_wunsch.py input.txt`

## Examples

1. Input file:
```
atgc
atgc
```
Output:
```
4
atgc
atgc
```
2. Input file:
```
atgc
tgc
```
Output:
```
2
atgc
-tgc
```
3. Input file:
```
atgc
atc
```
Output:
```
2
atgc
at-c
```
4. Input file:
```
tatgc
acgcaa
```
Output:
```
0
tatgc--
-acgcaa
```

## Solution

My implementation of the Needleman–Wunsch algorithm is the Python script [`needleman_wunsch.py`](needleman_wunsch.py) with slightly extended functionality.
