import os
import re

# Dictionary that contains all the occurrences of the words in the ham emails
counter_ham = dict()
# Dictionary that contains all the occurrences of the words in the spam emails
counter_spam = dict()


# Function that reads all the emails, breaks the message in single words, counts the files and the occurrences of the words in the emails
def readWords(ham_loc, spam_loc):

    ham_total = len(os.listdir(os.getcwd()+ham_loc))
    spam_total = len(os.listdir(os.getcwd()+spam_loc))

    # For every file read the message break it down to single words (no duplicates of words) and update the dictionaries
    for fname in os.listdir(os.getcwd()+ham_loc):
        filename = os.getcwd()+ham_loc+fname
        file = open(filename, "r")
        message = file.read()
        contents = re.split("\s", message)
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in counter_ham:
                counter_ham.update({word: 1})
            else:
                counter_ham[word] = counter_ham.get(word)+1
        file.close()

    for fname in os.listdir(os.getcwd()+spam_loc):
        filename = os.getcwd() + spam_loc+ fname
        file = open(filename, "r")
        message = file.read()
        contents = re.split("\s", message)
        one_occur = []
        for word in contents:
            if word not in one_occur:
                one_occur.append(word)
        for word in one_occur:
            if word not in counter_spam:
                counter_spam.update({word: 1})
            else:
                counter_spam[word] = counter_spam.get(word) + 1
        file.close()

    return ham_total, spam_total


# Naive Bayes classifier
def classify(filename, ham_total, spam_total):

    # Open the file & finds what words of the message are in the dictionaries
    opened_file = open(filename, "r")
    message = opened_file.read()
    contents = re.split("\s", message)

    ham_total += 1
    spam_total += 1

    # We calculate the probabilities of the message
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

    # If the probability of ham is bigger or equal to the probability of spam return 1, else 0
    if final_ham >= final_spam:
        return 1
    elif final_ham < final_spam:
        return 0


# Helper function that is call from analysis contains the locations of the ham & spam trains, test & validation
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

    # Calculate accuracy, error, precision, recall & F1 and return them to analysis

    accuracy = correct_test/test_size*100

    error = 100 - accuracy

    precision = true_positive/(true_positive+false_positive)*100

    recall = true_positive/(true_positive+false_negative)*100

    f1 = 2*((precision*recall)/(precision+recall))

    return accuracy, error, precision, recall, f1
