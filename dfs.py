from wordle import Wordle
import statistics as st

tests = 1000
set = []
num_under_six = 0

for i in range(tests):
    w = Wordle()
    sum = 0
    while not w.is_guessed():
        sum += 1
        w.guess(w.get_possible()[0])
    set.append(sum)
    if sum <= 6:
        num_under_six += 1

print (st.mean(set), num_under_six/tests)
