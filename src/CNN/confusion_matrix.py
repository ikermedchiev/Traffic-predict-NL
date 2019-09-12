import parameters

total_actual = []
total_prediction = []

for day in range(14, 22):
    with open(parameters.ROOT_DIR + '/data/Files_A4/2018-03-' + str(day).zfill(2) + '.txt', 'r') as f:
        actual = f.read().split(',')
        actual = list(map(int, actual))

    with open(parameters.ROOT_DIR + '/results/2018-03-' + str(day).zfill(2) + '.txt', 'r') as f:
        predicted = f.read().split(',')
        predicted = list(map(float, predicted))

    total_actual.extend(actual[parameters.HISTORY + parameters.FUTURE:])
    total_actual.extend([0] * parameters.FUTURE)
    total_prediction.extend([p > 0.5 for p in predicted])

confusion_matrix = [[0, 0], [0, 0]]

for i in range(len(total_actual)):
    actual = total_actual[i]
    predicted = total_prediction[i]
    confusion_matrix[actual][predicted] += 1

for i in range(2):
    for j in range(2):
        print("Actual {}, Predicted {}: {}".format(i, j, confusion_matrix[i][j]))
