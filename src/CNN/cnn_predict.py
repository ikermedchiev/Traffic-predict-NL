import cnn_congestion
import pickle
import tensorflow as tf
import data_input
import parameters


def main(unused_argv):
    # Create the Estimator
    print('Create estimator')
    model_classifier = tf.estimator.Estimator(model_fn=cnn_congestion.cnn_model_fn,
                                              model_dir=parameters.ROOT_DIR +
                                                        '/tmp/bsize_' +
                                                        str(parameters.BATCHSIZE) +
                                                        '_hist_' +
                                                        str(parameters.HISTORY) +
                                                        '_futr_' +
                                                        str(parameters.FUTURE) +
                                                        '_lr_' +
                                                        str(parameters.LEARNINGRATE))

    for day in range(14, 22):
        filename = parameters.ROOT_DIR + '/pickled/2018-03-' + str(day).zfill(2) + \
                                         '_hist_' + str(parameters.HISTORY) + '.pickle'
        try:
            with open(filename, 'rb') as f:
                img_list = pickle.load(f)
        except FileNotFoundError:
            img_list = []
            for minute in range(parameters.HISTORY, 900):
                print("Retrieving image {}".format(minute))
                img = data_input.image_object(2018, 3, day, minute, parameters.HISTORY,parameters.FUTURE,
                                              parameters.NORMALIZED, parameters.NORM_FLOW,
                                              parameters.NORM_SPEED)
                img_list.append(img)
            with open(filename, 'wb') as f:
                pickle.dump(img_list, f, pickle.HIGHEST_PROTOCOL)

        predict_data, predict_labels = data_input.image_list_to_np_array(img_list)

        # Predict with the model and save results
        print('Predict with model')
        predict_input_fn = tf.estimator.inputs.numpy_input_fn(
            x={"x": predict_data},
            shuffle=False)
        predict_results = model_classifier.predict(input_fn=predict_input_fn)

        predicted = predict_results

        congestion_prob = []
        for minute in predicted:
            congestion_prob.append(minute.get("probabilities")[1])

        with open(parameters.ROOT_DIR + "/results/2018-03-" + str(day).zfill(2) + '.txt', 'w') as file:
            congestion_prob = list(map(str, congestion_prob))
            file.write(",".join(congestion_prob))


if __name__ == "__main__":
    tf.app.run()
