import matplotlib.pyplot as plt
import numpy as np
import naive_bayes as nb
import id3 as dt

enron1 = "/enron1"
enron2 = "/enron2"
enron3 = "/enron3"
enron4 = "/enron4"
enron5 = "/enron5"
enron6 = "/enron6"

train_ham = "/train/ham/"
train_spam = "/train/spam/"

test = "/test/"

validation = "/validate/"

def main():
    print("Naive Bayes Results:")
    accuracy1, error1, precision1, recall1, f11 = nb.init(enron1+train_ham, enron1+train_spam, enron1+train_ham, enron1+validation)
    print("Accuracy: ", accuracy1)
    print("Error: ", error1)
    print("Precision: ", precision1)
    print("Recall: ", recall1)
    print("F1: ", f11)

    print("\nID3 Results:")
    accuracy, error, precision, recall, f1 = dt.init(enron1 + train_ham, enron1 + train_spam, enron1 + train_ham, enron1 + validation)
    print("Accuracy: ", accuracy)
    print("Error: ", error)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)

    n_groups = 2

    accuracies = (accuracy1, accuracy)
    errors = (error1, error)
    precisions = (precision1, precision)
    recalls = (recall1, recall)
    f1s = (f11, f1)

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.1

    opacity = 1
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, accuracies, bar_width,
                    alpha=opacity, color='b',
                    error_kw=error_config,
                    label='Accuracy')

    rects2 = ax.bar(index + bar_width, errors, bar_width,
                    alpha=opacity, color='r',
                    error_kw=error_config,
                    label='Error')

    rects3 = ax.bar(index + bar_width + bar_width, precisions, bar_width,
                    alpha=opacity, color='darkorange',
                    error_kw=error_config,
                    label='Precision')

    rects4 = ax.bar(index + bar_width + bar_width + bar_width, recalls, bar_width,
                    alpha=opacity, color='yellow',
                    error_kw=error_config,
                    label='Recall')

    rects5 = ax.bar(index + bar_width + bar_width + bar_width + bar_width, f1s, bar_width,
                    alpha=opacity, color='g',
                    error_kw=error_config,
                    label='F1')

    ax.set_xlabel('Algorithms')
    ax.set_ylabel('Scores')
    ax.set_title('Scores of Machine Learning Algorithms')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('Naive Bayes', 'ID3'))
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()