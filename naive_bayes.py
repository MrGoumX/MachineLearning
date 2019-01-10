import os
import re

#ham = "/enron2/ham/"
#spam = "/enron2/spam/"

counter_ham = dict()
counter_spam = dict()

def readWords(ham_loc, spam_loc):

    ham_total = 0
    spam_total = 0

    for fname in os.listdir(os.getcwd()+ham_loc):
        filename = os.getcwd()+ham_loc+fname
        file = open(filename, "r")
        message = file.read()
        contents = re.split(" | \r\n", message)
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in counter_ham:
                counter_ham.update({word: 1})
            else:
                counter_ham[word] = counter_ham.get(word)+1
        ham_total += 1
        file.close()

    for fname in os.listdir(os.getcwd()+spam_loc):
        filename = os.getcwd() + spam_loc+ fname
        file = open(filename, "r")
        message = file.read()
        contents = message.split(" ")
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in counter_spam:
                counter_spam.update({word: 1})
            else:
                counter_spam[word] = counter_spam.get(word) + 1
        spam_total += 1
        file.close()

    return ham_total, spam_total

def classify(filename, ham_total, spam_total):

    opened_file = open(filename, "r")
    message = opened_file.read()
    contents = message.split(" ")

    ham_total += 1
    spam_total += 1

    final_spam = spam_total / (spam_total + ham_total)
    final_ham = ham_total / (spam_total + ham_total)

    for word in contents:
        ham = counter_ham.get(word)
        spam = counter_spam.get(word)
        if ham is None:
            ham = 1
        else:
            ham += 1
        if spam is None:
            spam = 1
        else:
            spam += 1

        final_spam *= (spam/spam_total)
        final_ham *= (ham/ham_total)

        if final_spam == 0 or final_ham == 0:
            break

    if final_ham >= final_spam:
        return 1
    elif final_ham < final_spam:
        return 0

def init(ham_train, spam_train, test, validation):

    ham_total, spam_total = readWords(ham_train, spam_train)

    test_size = len(os.listdir(os.getcwd()+test))

    correct_test = 0

    true_positive = 0
    false_positive = 0
    false_negative = 0

    for file in os.listdir(os.getcwd()+test):
        res = classify(os.getcwd()+test+file, ham_total, spam_total)

        if "spam" in file and res == 0:
            correct_test += 1
            true_positive += 1
        if "ham" in file and res == 1:
            correct_test += 1
            true_positive += 1
        if "spam" in file and res == 1:
            false_positive += 1
        if "ham" in file and res == 0:
            false_positive += 1

    validation_size = len(os.listdir(os.getcwd()+validation))

    correct_validation = 0

    for file in os.listdir(os.getcwd()+validation):

        res = classify(os.getcwd()+validation+file, ham_total, spam_total)

        if "spam" in file and res == 0:
            correct_validation += 1
            true_positive += 1
        if "ham" in file and res == 1:
            correct_validation += 1
            true_positive += 1
        if "spam" in file and res == 1:
            false_negative += 1
        if "ham" in file and res == 0:
            false_negative += 1

    accuracy = correct_test/test_size

    error = 1 - accuracy

    precision = true_positive/(true_positive+false_positive)

    recall = true_positive/(true_positive+false_negative)

    f1 = 2*((precision*recall)/(precision+recall))

    return accuracy, error, precision, recall, f1
