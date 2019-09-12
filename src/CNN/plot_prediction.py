import matplotlib.pyplot as plt
import parameters

plt.figure(figsize=(10, 25))

for day in range(14, 22):
    with open(parameters.ROOT_DIR + '/data/Files_A4/2018-03-' + str(day).zfill(2) + '.txt', 'r') as f:
        actual = f.read().split(',')
        actual = list(map(int, actual))

    with open(parameters.ROOT_DIR + '/results/2018-03-' + str(day).zfill(2) + '.txt', 'r') as f:
        predicted = f.read().split(',')
        predicted = list(map(float, predicted))

    actual_time = list(range(0, 900))
    predicted_time = list(range(parameters.HISTORY + parameters.FUTURE, 900 + parameters.FUTURE))

    plt.subplot(8, 1, day-13)
    plt.fill_between(actual_time, 0, actual, facecolor='red', alpha=0.1)
    plt.plot(actual_time, actual, 'r--', label='Actual data')
    plt.plot(predicted_time, predicted, 'b', label='Predicted data')
    plt.plot([0, 900 + parameters.FUTURE], [0.5, 0.5], 'k-', alpha=0.5)
    plt.xlabel("Time from 6:00 (minutes)")
    plt.ylabel("Congestion probability")
    plt.title("Congestion probability on 2018-03-" + str(day))
    plt.xlim(0, 900 + parameters.FUTURE)
    plt.ylim(0, 1.1)
    plt.yticks([0, 0.25, 0.5, 0.75, 1])
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout(pad=1, w_pad=1, h_pad=2)
plt.savefig(parameters.ROOT_DIR + '/results/figures/bsize_' + str(parameters.BATCHSIZE) +
            '_hist_' + str(parameters.HISTORY) +
            '_futr_' + str(parameters.FUTURE) +
            '_lr_' + str(parameters.LEARNINGRATE) + '.png')
