import os
import numpy as np

ham = "/enron2/ham/"
spam = "/enron2/spam/"

counter_ham = dict()
counter_spam = dict()
all_words = dict()
occur_ham = dict()
occur_spam = dict()

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

    for word in counter_ham:
        if word not in all_words:
            all_words[word] = counter_ham.get(word)
        else:
            all_words[word] = counter_ham.get(word) + all_words.get(word)

    for word in counter_spam:
        if word not in all_words:
            all_words[word] = counter_spam.get(word)
        else:
            all_words[word] = counter_spam.get(word) + all_words.get(word)


    words_count = 0
    for word in all_words:
        words_count += all_words.get(word)

    s_words_count = 0
    for word in counter_spam:
        s_words_count += counter_spam.get(word)

    h_words_count = 0
    for word in counter_ham:
        h_words_count += counter_ham.get(word)

    # entropy = -spam_total / (spam_total + ham_total) * np.log2(spam_total / (spam_total + ham_total)) - ham_total / (
    #             spam_total + ham_total) * np.log2(ham_total / (spam_total + ham_total))

    entropy = -(s_words_count/words_count)*np.log2(s_words_count/words_count) - (h_words_count/words_count)*np.log2(h_words_count/words_count)
    print(entropy)

    info_gain_spam = dict()
    info_gain_ham = dict()

    for word in all_words:
        temp_sum = 0
        if word in counter_ham:
            temp_sum += counter_ham.get(word)
        if word in counter_spam:
            temp_sum += counter_spam.get(word)
        temp_sum += 2

        word_ham = 1
        if word in counter_ham:
            word_ham += counter_ham.get(word)

        word_spam = 1
        if word in counter_spam:
            word_spam += counter_spam.get(word)

        entropy_ham = -((word_ham)/temp_sum)*np.log2((word_ham)/temp_sum)
        #print(entropy_ham)
        entropy_spam = -((word_spam)/temp_sum)*np.log2((word_spam)/temp_sum)

        #temp_div = all_words.get(word)
        occur_ham_word = 1
        if word in occur_ham:
            occur_ham_word += occur_ham.get(word)

        occur_spam_word = 1
        if word in occur_spam:
            occur_spam_word += occur_spam.get(word)

        temp_div = (occur_spam_word+occur_ham_word)/(ham_total+spam_total+2)

        #print(temp_div*entropy_ham)

        gain_ham = entropy - temp_div*entropy_ham
        gain_spam = entropy - temp_div*entropy_spam

        info_gain_ham[word] = gain_ham
        info_gain_spam[word] = gain_spam

    return info_gain_spam



if __name__ == '__main__':
    info_gain_spam = readWords()