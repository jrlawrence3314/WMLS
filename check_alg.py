from wordle import Wordle
import statistics as st
import csv

def find_highest(d, keys):
    filtered_dict = { key: d[key] for key in keys }

    return max(filtered_dict, key=filtered_dict.get)

w = Wordle()

word_dict = {}

with open("dict.csv", 'r') as inp:
    reader = csv.reader(inp)
    word_dict = {rows[0]:float(rows[1]) for rows in reader}

times_to_run = 100

guess_count = []

for i in range(times_to_run):
    w = Wordle()
    count = 0
    while not w.is_guessed():
        count += 1
        guess = find_highest(word_dict, w.get_possible())
        w.guess(guess)

    guess_count.append(count)
    if i % 10 == 0:
        print(i/times_to_run, count)

print(st.mean(guess_count))
