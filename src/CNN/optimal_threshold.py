import parameters
import matplotlib.pyplot as plt


def savediv(a, b):
    if a == 0:
        return 0
    elif b == 0:
        raise ZeroDivisionError
    else:
        return a / b


total_actual = []
total_prob = []

for day in range(14, 22):
    with open(parameters.ROOT_DIR + '/data/Files_A4/2018-03-' + str(day).zfill(2) + '.txt', 'r') as f:
        actual = f.read().split(',')
        actual = list(map(int, actual))

    total_actual.extend(actual[parameters.HISTORY + parameters.FUTURE:])
    total_actual.extend([0] * parameters.FUTURE)

    with open(parameters.ROOT_DIR + '/results/2018-03-' + str(day).zfill(2) + '.txt', 'r') as f:
        predicted = f.read().split(',')
        predicted = list(map(float, predicted))

    total_prob.extend(predicted)

threshold = [thr / 100 for thr in range(101)]
accuracy = []  # Percentage right
PPV = []  # Percentage of true positives over all predicted positives (positive predictive value / precision)
NPV = []  # Percentage of true negatives over all predicted negatives (negative predictive value)
TPR = []  # Percentage of true positives over all actual positives (true positive rate / sensitivity)
TNR = []  # Percentage of true negatives over all actual negatives (true negative rate / specificity)

for thr in threshold:

    total_prediction = [p > thr for p in total_prob]

    confusion_matrix = [[0, 0], [0, 0]]

    for i in range(len(total_actual)):
        actual = total_actual[i]
        predicted = total_prediction[i]
        confusion_matrix[actual][predicted] += 1

    TN = confusion_matrix[0][0]
    FP = confusion_matrix[0][1]
    FN = confusion_matrix[1][0]
    TP = confusion_matrix[1][1]

    accuracy.append(savediv(TN + TP, TN + FP + FN + TP))
    PPV.append(savediv(TP, TP + FP))
    NPV.append(savediv(TN, TN + FN))
    TPR.append(savediv(TP, TP + FN))
    TNR.append(savediv(TN, TN + FP))

plt.figure(figsize=[10, 5])

plt.plot(threshold, accuracy, label='Accuracy')
plt.plot(threshold, PPV, label='Positive predictive value = P(C|c)')
plt.plot(threshold, NPV, label="Negative predictive value = P(C'|c')")
plt.plot(threshold, TPR, label='True positive rate = P(c|C)')
plt.plot(threshold, TNR, label="True negative rate = P(c'|C')")

plt.xlabel('Threshold')
plt.ylabel('Percentage')
plt.xlim(0, 1)
plt.ylim(0, 1)
lgd = plt.legend(loc="upper left", bbox_to_anchor=[1, 1], title="C = actual congestion, c' = prediction no congestion")

plt.xticks([x/10 for x in range(11)])
plt.grid()
plt.show()

# plt.savefig(parameters.ROOT_DIR + '/results/figures/threshold_futr_' + str(parameters.FUTURE) + '.png',
#             bbox_extra_artists=(lgd,), bbox_inches='tight')
