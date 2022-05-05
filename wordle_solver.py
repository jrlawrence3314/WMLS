from wordle import Wordle
import statistics as st
import csv
import math as mt

w = Wordle()

times_to_run = int(len(w.answer_list) / 10) - 1

list = []
failures = 0

for i in range(times_to_run):
    w = Wordle()
    w.word = w.answer_list[i * 10]
    count = 0
    while not w.is_guessed():
        count += 1
        if count == 1: #quick guess
            w.guess(w.get_best_first_guess())
        elif count == 2:
            w.guess(w.get_second_guess())
        else:
            w.guess(w.get_deep_guess())

    list.append(count)
    if count > 6:
        failures += 1

    if i % 10 == 0:
        print(i/times_to_run, count)

print("Final: ", st.mean(list), ", ", failures )
