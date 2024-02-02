import argparse
import json
from statistics import mean

def pretty_print(o):
    print(json.dumps(o, indent=2))

def print_ranking(names, scores, description, addendum = ""):
    print(f"Sorted by {description}:\n{addendum}")
    for i in range(len(names)):
        if type(scores[i]) is float:
            print(f"{i+1}.\t{chars[i]}\t{scores[i]:.1f}")
        else:
            print(f"{i+1}.\t{chars[i]}\t{scores[i]}")
    print()

def sort_dictionary_by_value(char_scores, reverse=False):
    tuples = []
    for char, score in char_scores.items():
        t = (char, score)
        tuples.append(t)

    tuples.sort(key = lambda x: x[1], reverse = reverse)

    chars = []
    scores = []
    for t in tuples:
        chars.append(t[0])
        scores.append(t[1])
    return chars, scores

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')

parser.add_argument('filename')

args = parser.parse_args()

with open(args.filename) as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]

char_counts = {}
char_placements = {}
for index, line in enumerate(lines):
    chars = line.split(',')
    for secondary_placement, char in enumerate(chars):
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1
        if char not in char_placements:
            char_placements[char] = []
        char_placements[char].append(index * (secondary_placement+1))

char_average_placements = {}

for char, placements in char_placements.items():
    char_average_placements[char] = sum(placements) / len(placements)

#print("Counts of each character:")
#pretty_print(char_counts)
#print("Average placement of each character:")
#pretty_print(char_average_placements)

char_scores = {}

for char in char_counts:
    average_placement = char_average_placements[char]
    count = char_counts[char]
    score = average_placement / count
    char_scores[char] = score

#print("Dividing the average placement by count:")
#pretty_print(char_scores)
#print()
print(f"Rankings based on {args.filename}")
print()

addendum = "(Score is calculated by dividing average placement by count)\n"
chars, scores = sort_dictionary_by_value(char_scores)
print_ranking(chars, scores, "score", addendum = addendum)

chars, counts = sort_dictionary_by_value(char_counts, reverse=True)
print_ranking(chars, counts, "count")

#chars, counts = sort_dictionary_by_value(char_average_placements)
#print_ranking(chars, counts, "average placement")
