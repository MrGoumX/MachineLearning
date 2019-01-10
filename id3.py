import os
import numpy as np
import re
from copy import deepcopy

# Treenode class
class Node(object):

    def __init__(self, parent=None, ham_prob=None, spam_prob=None):
        self.parent = parent
        self.ham_prob = ham_prob
        self.spam_prob = spam_prob
        self.left = None
        self.right = None
        self.word = None

    def print(self):
        print(self.get_probs())
        #os.system("pause")
        if self.left is not None:
            self.left.print()
        if self.right is not None:
            self.right.print()

    def name(self, word):
        self.word = word

    def insert_left(self, node):
        self.left = node

    def insert_right(self, node):
        self.right = node

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_probs(self):
        return self.ham_prob, self.spam_prob

    def get_word(self):
        return self.word

    def get_parent(self):
        return self.parent


# Files locations
ham_loc = "/enron2/ham/"
spam_loc = "/enron2/spam/"

# All ham emails
ham_emails = []
# All spam emails
spam_emails = []
# Words that occur in ham emails and their population
ham_occurs = dict()
# Words that occur in spam emails and their population
spam_occurs = dict()
# Words that occur in all emails and their population
all_words = dict()
# Total number of emails
total_count = 0
# Total number of ham emails
ham_count = 0
# Total number of spam emails
spam_count = 0
# Entropy is entrop[0], global variable
entrop = []

def readWords():

    # Ham and spam email numbers
    ham_count = 0
    spam_count = 0

    for fname in os.listdir(os.getcwd()+ham_loc):
        filename = os.getcwd()+ham_loc+"/"+fname
        file = open(filename, "r")
        # message of mail as string
        message = file.read()
        # list of words
        contents = re.split(" | \r\n", message)
        # list that has only the words and not the duplicates
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in ham_occurs:
                ham_occurs.update({word: 1})
            else:
                ham_occurs[word] = ham_occurs.get(word) + 1
        ham_count += 1
        ham_emails.append(one_occur)
        file.close()

    for fname in os.listdir(os.getcwd()+spam_loc):
        filename = os.getcwd()+spam_loc+"/"+fname
        file = open(filename, "r")
        message = file.read()
        contents = re.split(" | \r\n", message)
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in spam_occurs:
                spam_occurs.update({word: 1})
            else:
                spam_occurs[word] = spam_occurs.get(word) + 1
        spam_count += 1
        spam_emails.append(one_occur)
        file.close()

    analogy_spam = 1
    analogy_ham = 1

    if spam_count < ham_count:
        analogy_spam = ham_count / spam_count
    else:
        analogy_ham = spam_count / ham_count

    for word in ham_occurs:
        all_words[word] = ham_occurs.get(word)*analogy_ham

    for word in spam_occurs:
        if word not in all_words:
            all_words[word] = spam_occurs.get(word)*analogy_spam
        else:
            all_words[word] = np.abs(all_words.get(word) - spam_occurs.get(word)*analogy_spam)

    to_desc = sorted(all_words, key=all_words.get, reverse=True)

    all_words_sorted = dict()

    for word in to_desc:
        all_words_sorted[word] = all_words.get(word)

    #print(analogy)

    percent = int(0.003 * len(all_words_sorted))

    print("-----------------------------------\nNumber of words: ", percent, "\n--------------------------------------------")

    most_imp = dict()

    for i in range(0, percent):
        #print(all_words_sorted[i], temp_d.get(all_words_sorted[i]))
        #print(all_words_sorted[i], all_words.get(all_words_sorted[i]))
        word = to_desc[i]
        #print(word, all_words.get(word)
        most_imp[word] = all_words.get(word)

    return ham_count, spam_count, most_imp

def util(word, ham_emails, spam_emails):

    ham_in = []
    ham_not_in = []
    spam_in = []
    spam_not_in = []

    if word is not None:
        for e in ham_emails:
            if word in e:
                ham_in.append(e)
            else:
                ham_not_in.append(e)
        for e in spam_emails:
            if word in e:
                spam_in.append(e)
            else:
                spam_not_in.append(e)
        all_words.pop(word, None)

    ham_count = len(ham_in)
    spam_count = len(spam_in)

    ham_occurs.clear()
    spam_occurs.clear()

    for i in ham_in:
        for word in i:
            if word not in ham_occurs:
                ham_occurs.update({word: 1})
            else:
                ham_occurs[word] = ham_occurs.get(word) + 1

    for i in spam_in:
        for word in i:
            if word not in spam_occurs:
                spam_occurs.update({word: 1})
            else:
                spam_occurs[word] = spam_occurs.get(word) + 1

    return ham_count, spam_count, ham_in, ham_not_in, spam_in, spam_not_in

def entropy(ham_total, spam_total):
    return -spam_total / (spam_total + ham_total) * np.log2(spam_total / (spam_total + ham_total)) - ham_total / (
                 spam_total + ham_total) * np.log2(ham_total / (spam_total + ham_total))

def ig(ham_total, spam_total, entropy, word):

    word_sum = 2
    if word in ham_occurs:
        word_sum += ham_occurs.get(word)
    if word in spam_occurs:
        word_sum += spam_occurs.get(word)

    total_emails = spam_total + ham_total + 0

    ham = 0
    spam = 0
    if word in ham_occurs:
        ham += ham_occurs.get(word)
    if word in spam_occurs:
        spam += spam_occurs.get(word)

    word_exists = word_sum/total_emails
    word_not_exists = (total_emails-word_sum)/total_emails

    not_exists_ham = (ham_total-ham)
    not_exists_spam = (spam_total-spam)

    temp_sum = not_exists_ham + not_exists_spam

    #print(word_not_exists)

    not_exists_ham = (not_exists_ham)/(temp_sum)
    not_exists_spam = (not_exists_spam)/(temp_sum)

    #print(temp_sum)

    exists_ham = (ham)/word_sum
    exists_spam = (spam)/word_sum

    c_not_ham = not_exists_ham*np.log2(not_exists_ham)
    c_not_spam = not_exists_spam*np.log2(not_exists_spam)

    c_ham = exists_ham*np.log2(exists_ham)
    c_spam = exists_spam*np.log2(exists_spam)

    not_sum = -(c_not_ham + c_not_spam)
    sum = -(c_ham + c_spam)

    ex = word_exists*sum
    not_ex = word_not_exists*not_sum

    ig = entropy - (ex + not_ex)

    #print(ig)

    return ig

test1 = []

def best_info_gain(ham_count, spam_count, most_imp):

    info_gain = dict()
    sorted_info_gain = dict()
    #ent = entropy(ham_count, spam_count)
    #print(ent)
    for word in most_imp:
        info_gain[word] = ig(ham_count, spam_count, entrop[0], word)

    sorted_words = sorted(info_gain, key=info_gain.get, reverse=True)
    for word in sorted_words:
        sorted_info_gain[word] = info_gain.get(word)
        #print(word, info_gain.get(word))
        #os.system("pause")

    best = list(sorted_info_gain)[0]

    return best

def id3(ham_emails, spam_emails, most_imp, root):

    ham_total = len(ham_emails)
    spam_total = len(spam_emails)

    if ham_total <= 0 or spam_total <= 0:
        return root

    if len(most_imp) == 0:
        return root

    if (ham_total + spam_total) < 100:
        return root

    best = best_info_gain(ham_total, spam_total, most_imp)

    #print(best)

    ham_count, spam_count, ham_in, ham_not_in, spam_in, spam_not_in = util(best, ham_emails, spam_emails)

    if len(ham_in) == 0 and len(spam_in) == 0:
        return root

    if len(ham_not_in) == 0 and len(spam_not_in) == 0:
        return root

    root.name(best)

    most_imp.pop(best, None)

    # Left include word, X = 0

    prob_ham_left = (len(ham_in))/((len(ham_in)+len(spam_in)))

    left = Node(root, prob_ham_left, 1 - prob_ham_left)

    if prob_ham_left >= 0.95 or prob_ham_left <= 0.05:
        root.insert_left(left)
    else:
        left = id3(ham_in, spam_in, most_imp, left)

        root.insert_left(left)

    # Right not include word, X = 0

    prob_ham_right = len(ham_not_in)/(len(ham_not_in)+len(spam_not_in))

    right = Node(root, prob_ham_right, 1 - prob_ham_right)

    if prob_ham_right >= 0.95 or prob_ham_right <= 0.05:
        root.insert_right(right)
    else:
        right = id3(ham_not_in, spam_not_in, most_imp, right)

        root.insert_right(right)

    return root

if __name__ == '__main__':

    ham_count, spam_count, most_imp = readWords()
    test1.append(entropy(ham_count, spam_count))
    # ham_count = ham_count
    # spam_count = spam_count
    # total_count = ham_count+spam_count
    # best = best_info_gain(ham_count, spam_count, most_imp)
    # most_imp.pop(best, None)
    # ham_count, spam_count = util(best)
    # best = best_info_gain(ham_count, spam_count, most_imp)
    # print(best)
    total_count = ham_count+spam_count
    #best = best_info_gain(ham_count, spam_count, most_imp)
    ham_freq = ham_count/total_count
    spam_freq = spam_count/total_count
    ent = entropy(ham_count, spam_count)
    entrop.append(ent)
    new_ham_emails = deepcopy(ham_emails)
    new_spam_emails = deepcopy(spam_emails)
    root = Node(None)
    root = id3(ham_emails, spam_emails, most_imp, root)
    left = root.get_left()
    right = root.get_right()
    #print("Success")
    #root.print()
    #print(ham_count, spam_count, best)
    test = os.getcwd()+"/enron1/spam/"
    f_ham = 0
    f_spam = 0
    for f in os.listdir(test):
        #print(f)
        file = open(test+f, "r")
        message = file.read()
        testing = re.split(" | \r\n", message)
        file_w = []
        for i in testing:
            if i in testing and i not in file_w:
                file_w.append(i)
        file.close()
        ham_r = 0
        spam_r = 0
        temp = root
        while temp is not None:
            #print(temp.get_right().get_word())
            #if temp.get_word() in file_w:
            if temp.get_word() in file_w:
                #print("Here")
                temp = temp.get_left()
                if temp.get_right() is None or temp.get_left() is None:
                    break
                #print(temp.get_word())
            else:
                temp = temp.get_right()
                if temp.get_right() is None or temp.get_left() is None:
                    break
                #print(temp.get_word())
            #else:
                #continue
        ham, spam = temp.get_probs()
        #print(ham, spam)
        if ham > spam:
            #print("Ham")
            f_ham += 1
        elif ham < spam:
            #print("Spam")
            f_spam += 1
        else:
            print('-')
    #print(temp.get_probs())
    print("Number of ham is: ", f_ham)
    print("Number of spam is: ", f_spam)