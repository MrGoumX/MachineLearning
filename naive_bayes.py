import os
import re

ham = "/enron2/ham/"
spam = "/enron2/spam/"

counter_ham = dict()
counter_spam = dict()

def readWords():

    ham_total = 0
    spam_total = 0

    for fname in os.listdir(os.getcwd()+ham):
        filename = os.getcwd()+ham+"/"+fname
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

    for fname in os.listdir(os.getcwd()+spam):
        filename = os.getcwd() + spam + fname
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

    if final_ham > final_spam:
        return "The message is ham"
    elif final_ham < final_spam:
        return "The message is spam"

if __name__ == '__main__':
    ham_total, spam_total = readWords()
    temp = "/enron1/ham"

    for file in os.listdir(os.getcwd() + temp):
        print(temp + file)
        answer = classify(os.getcwd() + temp + "/" + file, ham_total, spam_total)
        print(answer)
