import os
import numpy as np

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

ham_loc = "/enron2/ham/"
spam_loc = "/enron2/spam/"

ham_emails = []
spam_emails = []
ham_occurs = dict()
spam_occurs = dict()
all_words = dict()
total_count = 0
ham_count = 0
spam_count = 0
f_words = []

def readWords():

    ham_count = 0
    spam_count = 0

    for fname in os.listdir(os.getcwd()+ham_loc):
        filename = os.getcwd()+ham_loc+"/"+fname
        file = open(filename, "r")
        message = file.read()
        contents = message.split(" ")
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
        contents = message.split(" ")
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

    for word in ham_occurs:
        if word not in all_words:
            all_words[word] = ham_occurs.get(word)
        else:
            all_words[word] = ham_occurs.get(word) + all_words.get(word)

    for word in spam_occurs:
        if word not in all_words:
            all_words[word] = spam_occurs.get(word)
        else:
            all_words[word] = np.abs(all_words.get(word) - spam_occurs.get(word))

    all_words_sorted = sorted(all_words, key=all_words.get, reverse=True)

    percent = int(0.001 * len(all_words_sorted))

    most_imp = dict()

    for i in range(0, percent):
        word = all_words_sorted[i]
        most_imp[word] = all_words.get(word)

    return ham_count, spam_count, most_imp

def util(word):

    if word is not None:
        for e in ham_emails:
            if word in e:
                ham_emails.remove(e)
        for e in spam_emails:
            if word in e:
                spam_emails.remove(e)
        all_words.pop(word, None)

    ham_count = len(ham_emails)
    spam_count = len(spam_emails)

    ham_occurs.clear()
    spam_occurs.clear()

    for i in ham_emails:
        for word in i:
            if word not in ham_occurs:
                ham_occurs.update({word: 1})
            else:
                ham_occurs[word] = ham_occurs.get(word) + 1

    for i in spam_emails:
        for word in i:
            if word not in spam_occurs:
                spam_occurs.update({word: 1})
            else:
                spam_occurs[word] = spam_occurs.get(word) + 1

    return ham_count, spam_count

def entropy(ham_total, spam_total):
    return -spam_total / (spam_total + ham_total) * np.log2(spam_total / (spam_total + ham_total)) - ham_total / (
                 spam_total + ham_total) * np.log2(ham_total / (spam_total + ham_total))

def ig(ham_total, spam_total, entropy, word):

    word_sum = 2
    if word in ham_occurs:
        word_sum += ham_occurs.get(word)
    if word in spam_occurs:
        word_sum += spam_occurs.get(word)

    total_emails = spam_total + ham_total + 2

    ham = 1
    spam = 1
    if word in ham_occurs:
        ham += ham_occurs.get(word)
    if word in spam_occurs:
        spam += spam_occurs.get(word)

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

test1 = []

def best_info_gain(ham_count, spam_count, most_imp):

    info_gain = dict()
    sorted_info_gain = dict()
    ent = entropy(ham_count, spam_count)
    #print(ent)
    for word in most_imp:
        info_gain[word] = ig(ham_count, spam_count, ent, word)

    sorted_words = sorted(info_gain, key=info_gain.get, reverse=True)
    for word in sorted_words:
        sorted_info_gain[word] = info_gain.get(word)
        # print(info_gain.get(word))

    best = list(sorted_info_gain)[0]

    return best

def probabilities(ham_count, spam_count, word):

    total_count = ham_count + spam_count

    word_in_ham = 1
    word_in_spam = 1

    if word in ham_occurs:
        word_in_ham = ham_occurs.get(word)
    if word in spam_occurs:
        word_in_spam = spam_occurs.get(word)

    total_occurs = word_in_spam + word_in_ham

    prob_word_in_ham = word_in_ham/(total_occurs+2)
    prob_word_in_spam = word_in_spam/(total_occurs+2)

    has_not_word = total_count - total_occurs

    not_in_ham = 1
    not_in_spam = 1

    for i in ham_emails:
        if word not in i:
            not_in_ham += 1

    for i in spam_emails:
        if word not in i:
            not_in_spam += 1

    prob_no_word_in_ham = not_in_ham/(has_not_word+2)
    prob_no_word_in_spam = not_in_spam/(has_not_word+2)

    return prob_word_in_ham, prob_word_in_spam, prob_no_word_in_ham, prob_no_word_in_spam

def id3(ham_total, spam_total, most_imp, root):

    if ham_total <=0 or spam_total <= 0:
        return root

    if len(most_imp) == 0:
        return root

    best = best_info_gain(ham_total, spam_total, most_imp)

    #print(best)

    ham_count, spam_count = util(best)

    root.name(best)

    prob_word_in_ham, prob_word_in_spam, prob_no_word_in_ham, prob_no_word_in_spam = probabilities(ham_count, spam_count, best)

    left = Node(root, prob_word_in_ham, prob_word_in_spam)
    right = Node(root, prob_no_word_in_ham, prob_no_word_in_spam)

    most_imp.pop(best, None)

    if prob_word_in_ham >= 0.95 or prob_no_word_in_spam >= 0.95:
        root.insert_left(left)
        #return root
    else:

        #most_imp.pop(best, None)

        #best = best_info_gain(ham_count, spam_count, most_imp)

        #left.name(best)

        left = id3(ham_count, spam_count, most_imp, left)

        root.insert_left(left)

    if prob_no_word_in_ham >= 0.95 or prob_no_word_in_spam >= 0.95:
        root.insert_right(right)
        #return root
    else:

        #if len(most_imp) == 0:
            #return root

        #most_imp.pop(best, None)

        #ham_count, spam_count = util(best)

        #best = best_info_gain(ham_count, spam_count, most_imp)

        #right.name(best)

        right = id3(ham_count, spam_count, most_imp, left)

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
    root = Node(None, ham_freq, spam_freq)
    root = id3(ham_count, spam_count, most_imp, root)
    left = root.get_left()
    right = root.get_right()
    print("Success")
    #root.print()
    #print(ham_count, spam_count, best)
    test = os.getcwd()+"/enron1/ham/"
    for f in os.listdir(test):
        #print(f)
        file = open(test+f, "r")
        message = file.read()
        testing = message.split(" ")
        file_w = []
        for i in testing:
            if i in testing and i not in file_w:
                file_w.append(i)
        file.close()
        ham_r = 0
        spam_r = 0
        temp = root
        while temp is not None:
            #if temp.get_word() in file_w:
            if temp.get_word() in file_w:
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
        ham, spam = temp.get_parent().get_probs()
        if ham > spam:
            print("Ham")
        elif ham < spam:
            print("Spam")
        else:
            print('-')
    #print(temp.get_probs())