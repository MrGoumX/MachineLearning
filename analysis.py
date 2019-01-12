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

    # Choose the dataset for train, test, validation from the choices above
    dataset = enron1
    validate = enron2

    # Print the results in console
    print("Naive Bayes Results:")
    bay_acc, bay_error, bay_precision, bay_recall, bay_f1 = nb.init(dataset+train_ham, dataset+train_spam, dataset+train_ham, validate+validation)
    print("Accuracy: ", bay_acc)
    print("Error: ", bay_error)
    print("Precision: ", bay_precision)
    print("Recall: ", bay_recall)
    print("F1: ", bay_f1)

    print("\nID3 Results:")
    id3_accuracy, id3_error, id3_precision, id3_recall, id3_f1 = dt.init(dataset + train_ham, dataset + train_spam, dataset + train_ham, validate + validation)
    print("Accuracy: ", id3_accuracy)
    print("Error: ", id3_error)
    print("Precision: ", id3_precision)
    print("Recall: ", id3_recall)
    print("F1: ", id3_f1)

    # Create the graph and show it
    n_groups = 2

    accuracies = (bay_acc, id3_accuracy)
    errors = (bay_error, id3_error)
    precisions = (bay_precision, id3_precision)
    recalls = (bay_recall, id3_recall)
    f1s = (bay_f1, id3_f1)

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