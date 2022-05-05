import sys
import random
import re
import copy
import math as mt
import csv
import time
import datetime as dt
import ast
import collections


class Wordle:
    def __init__(self):
        with open("wordle_answers.txt") as word_list:
            list = word_list.read() # import wordle list
        self.answer_list = []
        for line in list.splitlines():
            self.answer_list.append(line)
        with open("wordle.txt") as word_list:
            list = word_list.read() # import wordle list
        self.word_list = []
        for line in list.splitlines():
            self.word_list.append(line)
        self.word = random.choice(self.answer_list)
        self.exclude = "" #guessed letters that are NOT in the word
        self.correct = "....." #replace dot with correct letter when guessed
        self.semi = "" # guessed letters that are somewhere in the word
        self.wrong_pos = ["", "", "", "", ""] #list of wrong places, i.e. "..i.." when i is anywhere else
        self.score = 0;
        self.guesses = {}

        self.log2 = {}
        leng = len(self.word_list)
        for i in range(1, len(self.word_list) + 1):
            self.log2[i] = mt.log2(i/leng)

    def set_word(self, word):
        self.word = word

    def get_word(self):
        return self.word

    def is_guessed(self):
        return self.correct == self.word

    def get_possible(self):
        possible = []
        regex = "^"
        # positive lookahead
        if len(self.semi) > 0:
            regex += "(?=[a-z]*["+self.semi+"])"
        # negative lookahead
        if len(self.exclude) > 0:
            regex += "(?![a-z]*["+self.exclude+"])"
        # word size
        regex += "[a-z]{5}$"

        regex2 = "^"
        for i in range(5):
            regex2 += "[^" + self.wrong_pos[i] + "1]"

        first_filter = re.compile(self.correct)
        second_filter = re.compile(regex)
        third_filter = re.compile(regex2)


        for word in self.word_list:
            if first_filter.match(word): # two part regex checking
                if second_filter.match(word): # checks exlude & semi
                    if third_filter.match(word):
                        possible.append(word)

        return possible

    def get_possible_answers(self):
        possible = []
        regex = "^"
        # positive lookahead
        if len(self.semi) > 0:
            for i in range(len(self.semi)):
                    regex += "(?=[a-z]*["+self.semi[i]+"])"
        # negative lookahead
        if len(self.exclude) > 0:
            regex += "(?![a-z]*["+self.exclude+"])"
        # word size
        regex += "[a-z]{5}$"

        regex2 = "^"
        for i in range(5):
            regex2 += "[^" + self.wrong_pos[i] + "1]"

        first_filter = re.compile(self.correct)
        second_filter = re.compile(regex)
        third_filter = re.compile(regex2)


        for word in self.answer_list:
            if first_filter.match(word): # two part regex checking
                if second_filter.match(word): # checks exlude & semi
                    if third_filter.match(word):
                        possible.append(word)

        return possible

    def reset_guesses(self):
        self.exclude = "" #guessed letters that are NOT in the word
        self.correct = "....." #replace dot with correct letter when guessed
        self.semi = "" # guessed letters that are somewhere in the word
        self.wrong_pos = ["", "", "", "", ""] #list of wrong places, i.e. "..i.." when i is anywhere else


    def calc_guess(self): #long
        w = copy.deepcopy(self)
        possible = self.get_possible_answers()
        answer_list = possible
        starttime = time.time()
        tot_len = len(possible)
        i = 0
        for guess_word in possible:
            i += 1
            # print(i / tot_len)
            self.guesses[guess_word] = 0
            ent = 0
            corr_list = copy.deepcopy(answer_list)
            while len(corr_list) > 0:
                w.reset_guesses()
                w.word = corr_list[0]
                w.guess(guess_word)
                new_possible = w.get_possible()
                new_len = len(new_possible)
                if new_len == 0:
                    break
                p = new_len / len(possible)
                ent -= p * self.log2[new_len]
                corr_list.remove(corr_list[0])
                for poss_word in new_possible:
                    if poss_word in corr_list:
                        corr_list.remove(poss_word)


            self.guesses[guess_word] += ent

        return self.guesses

    def calcProcessTime(self, starttime, cur_iter, max_iter):

        telapsed = time.time() - starttime
        testimated = (telapsed/cur_iter)*(max_iter)

        finishtime = starttime + testimated
        finishtime = dt.datetime.fromtimestamp(finishtime).strftime("%H:%M:%S")  # in time

        lefttime = testimated-telapsed  # in seconds

        return (int(telapsed), int(lefttime), finishtime)

    def calc_second_guess(self): #long
        w = copy.deepcopy(self)
        possible = self.get_possible()
        answer_list = self.get_possible_answers()
        starttime = time.time()
        tot_len = len(possible)
        i = 0
        for guess_word in possible:
            i += 1
            if i%3 == 0:
                print(i / tot_len, self.calcProcessTime(starttime, i, tot_len))
            self.guesses[guess_word] = 0
            ent = 0
            corr_list = copy.deepcopy(answer_list)
            while len(corr_list) > 0:
                w.reset_guesses()
                w.word = corr_list[0]
                w.guess('cruel') #generated best first word
                w.guess(guess_word)
                new_possible = w.get_possible_answers()
                new_len = len(new_possible)
                if new_len == 0:
                    break
                p = new_len / len(possible)
                ent -= p * self.log2[new_len]
                corr_list.remove(corr_list[0])
                for poss_word in new_possible:
                    if poss_word in corr_list:
                        corr_list.remove(poss_word)


            self.guesses[guess_word] += ent

        return self.guesses

    def get_entropy_data(self):
        guesses = self.calc_guess()
        keys = guesses.keys()

        with open('entrop.csv', 'w') as f:
            for key in guesses.keys():
                f.write("%s, %s\n" % (key, guesses[key]))

    def load_entropy_data(self):
        with open('entropy.csv', 'r') as d:
            reader = csv.reader(d)
            out = {rows[0]:float(rows[1]) for rows in reader}

        return out

    def load_second_entropy_data(self):
        with open('entropy2.csv', 'r') as d:
            reader = csv.reader(d)
            out = {rows[0]:float(rows[1]) for rows in reader}
        return out

    def get_best_first_guess(self):
        list = self.load_entropy_data()
        return max(list, key=list.get)

    def get_second_guess(self):
        possible = self.get_possible()
        entropy_dict = self.load_second_entropy_data()
        list = {}
        for guess in possible:
            list[guess] = entropy_dict[guess]

        return max(list, key=list.get)

    def get_deep_guess(self): #recommended for first two guesses
        self.calc_guess()
        possible = self.get_possible_answers()
        list = {}
        for guess in possible:
            if guess in self.guesses:
                list[guess] = self.guesses[guess]

        return max(list, key=list.get)

    def user_guess(self, word, positions):
        out = ast.literal_eval(positions)
        for i in range(len(word)):
            if out[i] == 1:
                self.semi += word[i]
                self.wrong_pos[i] += word[i]

            elif out[i] == 0:
                for j in range(len(word)):
                    if word[i] not in self.semi and word[i] not in self.correct:
                        self.exclude += word[i]
            else:
                new_str = ""
                for j in range(len(word)):
                    if j != i:
                        new_str += self.correct[j]
                    else:
                        new_str += word[j]

                self.correct = new_str
        return "success"

    def guess(self, word):
        #implement
        self.score -= 10
        out = [0, 0, 0, 0, 0]

        if len(word) != 5:
            return "ERROR"
        if word not in self.word_list:
            return "INVALID GUESS"
        for i in range(len(word)):
            if word[i] in self.word:
                out[i] += 1

                if word[i] is self.word[i]:
                    out[i] += 1

        for i in range(len(word)):
            if out[i] == 1:
                self.semi += word[i]
                self.wrong_pos[i] += word[i]

            elif out[i] == 0:
                for j in range(len(word)):
                    self.exclude += word[i]
            else:
                new_str = ""
                for j in range(len(word)):
                    if j != i:
                        new_str += self.correct[j]
                    else:
                        new_str += word[j]

                self.correct = new_str

        return out
