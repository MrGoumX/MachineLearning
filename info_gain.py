from collections import OrderedDict
import os
import numpy as np

class Node:

    def __init__(self, parent, ham_value, spam_value, sum_value):
        self.parent = parent
        self.left = None
        self.right = None
        self.ham_value = ham_value
        self.spam_value = spam_value
        self.sum_value = sum_value

    def insert(self, left, right):
        self.left = left
        self.right = right

    def print(self):
        if self.left:
            self.left.print()
        print(self.ham_value, self.spam_value)
        if self.right:
            self.right.print()

    def printResult(self):
        if self.left:
            self.left.printResult()
        if self.right:
            self.right.printResult()
        if self.left is None and self.right is None:
            if self.ham_value > self.spam_value:
                print("Message is Ham")
            elif self.ham_value < self.spam_value:
                print("Message is Spam")

ham = "/enron2/ham/"
spam = "/enron2/spam/"

counter_ham = dict()
counter_spam = dict()
all_words = dict()
occur_ham = dict()
occur_spam = dict()
f_words = []
f_emails = 0
f_ham = 0
f_spam = 0

def readWords():

    ham_total = 0
    spam_total = 0

    for fname in os.listdir(os.getcwd()+ham):
        filename = os.getcwd()+ham+"/"+fname
        file = open(filename, "r")
        message = file.read()
        contents = message.split(" ")
        for word in contents:
            if word not in counter_ham:
                counter_ham.update({word: 1})
            else:
                counter_ham[word] = counter_ham.get(word) + 1
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in occur_ham:
                occur_ham.update({word: 1})
            else:
                occur_ham[word] = occur_ham.get(word) + 1
        ham_total += 1
        file.close()

    for fname in os.listdir(os.getcwd()+spam):
        filename = os.getcwd() + spam + fname
        file = open(filename, "r")
        message = file.read()
        contents = message.split(" ")
        for word in contents:
            if word not in counter_spam:
                counter_spam.update({word: 1})
            else:
                counter_spam[word] = counter_spam.get(word) + 1
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in occur_spam:
                occur_spam.update({word: 1})
            else:
                occur_spam[word] = occur_spam.get(word) + 1
        spam_total += 1
        file.close()

    for word in occur_ham:
        if word not in all_words:
            all_words[word] = occur_ham.get(word)
        else:
            all_words[word] = occur_ham.get(word) + all_words.get(word)

    for word in occur_spam:
        if word not in all_words:
            all_words[word] = occur_spam.get(word)
        else:
            all_words[word] = np.abs(all_words.get(word) - occur_spam.get(word))
            #all_words[word] = all_words.get(word) + occur_spam.get(word)

    entropy = -spam_total / (spam_total + ham_total) * np.log2(spam_total / (spam_total + ham_total)) - ham_total / (
                 spam_total + ham_total) * np.log2(ham_total / (spam_total + ham_total))

    #print(entropy)
    #os.system("pause")

    all_words_sorted = sorted(all_words, key=all_words.get, reverse=True)

    percent = int(0.005*len(all_words_sorted))

    most_imp = dict()

    for i in range(0, percent):
        word = all_words_sorted[i]
        #print(word)
        most_imp[word] = all_words.get(word)

    info_gain = dict()

    for word in most_imp:

        exists = most_imp.get(word)/(spam_total+ham_total)
        non_exists = 1 - exists

        entr_ex = entropy*exists
        entr_non_ex = entropy*non_exists

        res = exists*entr_ex + non_exists*entr_non_ex

        ig = entropy - res

        info_gain[word] = ig
        #print(ig)

    return ham_total, spam_total, most_imp

def ig(ham_total, spam_total, entropy, word):

    word_sum = 2
    if word in occur_ham:
        word_sum += occur_ham.get(word)
    if word in occur_spam:
        word_sum += occur_spam.get(word)

    total_emails = spam_total + ham_total + 2

    ham = 1
    spam = 1
    if word in occur_ham:
        ham += occur_ham.get(word)
    if word in occur_spam:
        spam += occur_spam.get(word)

    word_exists = word_sum/total_emails
    word_not_exists = (total_emails-word_sum)/total_emails

    not_exists_ham = (total_emails-ham)/(total_emails+1)
    not_exists_spam = (total_emails-spam)/(total_emails+1)

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


def entropy(ham_total, spam_total):
    return -spam_total / (spam_total + ham_total) * np.log2(spam_total / (spam_total + ham_total)) - ham_total / (
                 spam_total + ham_total) * np.log2(ham_total / (spam_total + ham_total))

def id3(entropy, ham_total, spam_total, sorted_ig, root):

    if len(sorted_ig) == 0:
        return

    if (ham_total+spam_total) == 0:
        return

    print(ham_total+spam_total)

    #print(len(sorted_ig))

    best = list(sorted_ig.keys())[0]
    f_words.append(best)
    ham_count = 1
    spam_count = 1
    if best in occur_ham:
        ham_count += (f_ham-occur_ham.get(best))
    if best in occur_spam:
        spam_count += (f_spam-occur_spam.get(best))
    count = ham_count+spam_count

    ham_value = ham_count/count
    spam_value = spam_count/count

    count_not = f_emails-count

    #ham_value_not = (spam_total+ham_total-ham_count+1)/(count_not+1)
    #spam_value_not = (spam_total + ham_total - spam_count+1) / (count_not+1)
    ham_value_not = (ham_total-ham_count)/(count_not+1)
    spam_value_not = (spam_total-spam_count)/(count_not+1)

    print(ham_value)
    print(spam_value)
    print(ham_value_not)
    print(spam_value_not)

    left = Node(root, ham_value, spam_value, count)
    right = Node(root, ham_value_not, spam_value_not, count_not)

    root.insert(left, right)

    sorted_ig.pop(best, None)

    for word in sorted_ig:
        if word is not None:
            sorted_ig[word] = ig(ham_count,  spam_count, entropy, word)
            #sorted_ig[word] = ig(ham_total, spam_total, entropy, word)

    sort = sorted(sorted_ig, key=sorted_ig.get, reverse=True)

    sorted_ig_new = dict()

    for word in sort:
        sorted_ig_new[word] = sorted_ig.get(word)
        #print(sorted_ig.get(word))
    print("------------------------------------------")
    #os.system("pause")

    #print(len(sorted_ig_new))

    left = id3(entropy, ham_count, spam_count, sorted_ig_new, left)
    #right = id3(entropy, ham_total, spam_total, sorted_ig_new, right)

    return root

if __name__ == '__main__':
    test = dict()
    test[1] = 1
    test[2] = 2
    test.pop(2, None)
    test.pop(1, None)
    print(len(test))
    #os.system("pause")
    ham_total, spam_total, most_imp = readWords()
    ham_percent = ham_total/(ham_total+spam_total)
    spam_percent = spam_total/(ham_total+spam_total)
    root = Node(None, ham_percent, spam_percent, ham_total+spam_total)
    info_gain = dict()
    f_emails = ham_total + spam_total
    f_ham = ham_total
    f_spam = spam_total
    ent = entropy(ham_total, spam_total)
    for word in most_imp:
        info_gain[word] = ig(ham_total, spam_total, ent, word)

    sort = sorted(info_gain, key=info_gain.get, reverse=True)

    sorted_ig = dict()

    for word in sort:
        sorted_ig[word] = info_gain.get(word)

    best = list(sorted_ig.keys())[0]
    print(best)
    #tree = id3(entropy(ham_total, spam_total), ham_total, spam_total, sorted_ig, root)
    #tree.print()
    print("Finished")

    # for i in info_gain_spam:
    #     print(info_gain_spam.get(i))
