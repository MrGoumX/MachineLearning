import os
import numpy as np
import re
from copy import deepcopy

np.seterr(divide='ignore', invalid='ignore')

# Tree node class
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


# Function that reads all the emails, breaks the message in single words, counts the files and the occurrences of the words in the emails, save all the email as an example for id3
def readWords(ham_loc, spam_loc):

    # Ham and spam email numbers
    ham_count = len(os.listdir(os.getcwd()+ham_loc))
    spam_count = len(os.listdir(os.getcwd()+spam_loc))

    # For every file read the message break it down to single words (no duplicates of words) and update the dictionaries
    for fname in os.listdir(os.getcwd()+ham_loc):
        filename = os.getcwd()+ham_loc+"/"+fname
        file = open(filename, "r")
        # message of mail as string
        message = file.read()
        # list of words
        contents = re.split("\s", message)
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
        ham_emails.append(one_occur)
        file.close()

    for fname in os.listdir(os.getcwd()+spam_loc):
        filename = os.getcwd()+spam_loc+"/"+fname
        file = open(filename, "r")
        message = file.read()
        contents = re.split("\s", message)
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in spam_occurs:
                spam_occurs.update({word: 1})
            else:
                spam_occurs[word] = spam_occurs.get(word) + 1
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

    # Calculate the best words for the tree creation

    to_desc = sorted(all_words, key=all_words.get, reverse=True)

    all_words_sorted = dict()

    for word in to_desc:
        all_words_sorted[word] = all_words.get(word)

    percent = int(0.001 * len(all_words_sorted))

    most_imp = dict()

    for i in range(0, percent):
        word = to_desc[i]
        most_imp[word] = all_words.get(word)

    return ham_count, spam_count, most_imp


# Function util, calculates & keep the emails that a word exists in ham & spam AND keep the emails that a wods DOES NOT exists in ham & spam emails
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


# Function that calculates the entropy
def entropy(ham_total, spam_total):
    return -spam_total / (spam_total + ham_total) * np.log2(spam_total / (spam_total + ham_total)) - ham_total / (
                 spam_total + ham_total) * np.log2(ham_total / (spam_total + ham_total))

# Function that calculates the informaion gain for a specific word
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

    not_exists_ham = (ham_total-ham)+1
    not_exists_spam = (spam_total-spam)+1

    temp_sum = not_exists_ham + not_exists_spam + 2

    not_exists_ham = (not_exists_ham)/(temp_sum)
    not_exists_spam = (not_exists_spam)/(temp_sum)

    exists_ham = (ham+1)/word_sum
    exists_spam = (spam+1)/word_sum

    c_not_ham = not_exists_ham*np.log2(not_exists_ham)
    c_not_spam = not_exists_spam*np.log2(not_exists_spam)

    c_ham = exists_ham*np.log2(exists_ham)
    c_spam = exists_spam*np.log2(exists_spam)

    not_sum = -(c_not_ham + c_not_spam)
    sum = -(c_ham + c_spam)

    ex = word_exists*sum
    not_ex = word_not_exists*not_sum

    ig = entropy - (ex + not_ex)

    return ig


# Function that returns from the most valuable words the on with the best information gain
def best_info_gain(ham_count, spam_count, most_imp):

    info_gain = dict()
    sorted_info_gain = dict()
    for word in most_imp:
        info_gain[word] = ig(ham_count, spam_count, entrop[0], word)

    sorted_words = sorted(info_gain, key=info_gain.get, reverse=True)
    for word in sorted_words:
        sorted_info_gain[word] = info_gain.get(word)

    best = list(sorted_info_gain)[0]

    return best

# Function that builds recursively the id3 decision tree
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

# Helper function that is call from analysis contains the locations of the ham & spam trains, test & validation
def init(ham_train, spam_train, test, validation):

    ham_count, spam_count, most_imp = readWords(ham_train, spam_train)

    total_count = ham_count + spam_count
    ham_freq = ham_count / total_count
    spam_freq = spam_count / total_count
    ent = entropy(ham_count, spam_count)
    entrop.append(ent)
    root = Node(None, ham_freq, spam_freq)
    root = id3(ham_emails, spam_emails, most_imp, root)

    test_size = len(os.listdir(os.getcwd() + test))

    correct_test = 0

    true_positive = 0
    false_positive = 0
    false_negative = 0

    for filename in os.listdir(os.getcwd() + test):

        new_tree = root

        file = open(os.getcwd() + test + filename, "r")
        message = file.read()
        testing = re.split(" | \r\n", message)
        file_w = []
        for i in testing:
            if i in testing and i not in file_w:
                file_w.append(i)
        file.close()

        while new_tree is not None:
            if new_tree.get_word() in file_w:
                new_tree = new_tree.get_left()
                if new_tree.get_right() is None or new_tree.get_left() is None:
                    break
            else:
                new_tree = new_tree.get_right()
                if new_tree.get_right() is None or new_tree.get_left() is None:
                    break
        ham, spam = new_tree.get_probs()
        if ham >= spam:
            res = 1
        else:
            res = 0

        if "spam" in filename and res == 0:
            correct_test += 1
            true_positive += 1
        if "ham" in filename and res == 1:
            correct_test += 1
            true_positive += 1
        if "spam" in filename and res == 1:
            false_positive += 1
        if "ham" in filename and res == 0:
            false_positive += 1

    validation_size = len(os.listdir(os.getcwd() + validation))

    correct_validation = 0

    for filename in os.listdir(os.getcwd() + validation):

        new_tree = root

        file = open(os.getcwd() + validation + filename, "r")
        message = file.read()
        testing = re.split(" | \r\n", message)
        file_w = []
        for i in testing:
            if i in testing and i not in file_w:
                file_w.append(i)
        file.close()

        while new_tree is not None:
            if new_tree.get_word() in file_w:
                new_tree = new_tree.get_left()
                if new_tree.get_right() is None or new_tree.get_left() is None:
                    break
            else:
                new_tree = new_tree.get_right()
                if new_tree.get_right() is None or new_tree.get_left() is None:
                    break
        ham, spam = new_tree.get_probs()
        if ham >= spam:
            res = 1
        else:
            res = 0

        if "spam" in filename and res == 0:
            correct_validation += 1
            true_positive += 1
        if "ham" in filename and res == 1:
            correct_validation += 1
            true_positive += 1
        if "spam" in filename and res == 1:
            false_negative += 1
        if "ham" in filename and res == 0:
            false_negative += 1

    accuracy = correct_test / test_size*100

    error = 100 - accuracy

    precision = true_positive / (true_positive + false_positive)*100

    recall = true_positive / (true_positive + false_negative)*100

    f1 = 2 * ((precision * recall) / (precision + recall))

    return accuracy, error, precision, recall, f1
