import numpy as np
import tensorflow as tf
import data_input
import parameters
import cnn_congestion


def main(flowdata, speeddata):
    # Create the Estimator
    print('Create estimators')
    model_classifier_5 = tf.estimator.Estimator(model_fn=cnn_congestion.cnn_model_fn,
                                                model_dir=parameters.ROOT_DIR +
                                                          '/tmp/bsize_' +
                                                          str(parameters.BATCHSIZE) +
                                                          '_hist_' +
                                                          str(parameters.HISTORY) +
                                                          '_futr_5' +
                                                          '_lr_' +
                                                          str(parameters.LEARNINGRATE))

    model_classifier_15 = tf.estimator.Estimator(model_fn=cnn_congestion.cnn_model_fn,
                                                 model_dir=parameters.ROOT_DIR +
                                                           '/tmp/bsize_' +
                                                           str(parameters.BATCHSIZE) +
                                                           '_hist_' +
                                                           str(parameters.HISTORY) +
                                                           '_futr_15' +
                                                           '_lr_' +
                                                           str(parameters.LEARNINGRATE))

    model_classifier_30 = tf.estimator.Estimator(model_fn=cnn_congestion.cnn_model_fn,
                                                 model_dir=parameters.ROOT_DIR +
                                                           '/tmp/bsize_' +
                                                           str(parameters.BATCHSIZE) +
                                                           '_hist_' +
                                                           str(parameters.HISTORY) +
                                                           '_futr_30' +
                                                           '_lr_' +
                                                           str(parameters.LEARNINGRATE))

    station_list = open(parameters.ROOT_DIR + '/data/measurementSiteIDs.txt').readlines()
    station_list = [line.strip() for line in station_list]

    flowdata = data_input.sort_image_rows(flowdata, station_list, float)
    speeddata = data_input.sort_image_rows(speeddata, station_list, float)

    if parameters.NORMALIZED:
        flowdata = list(map(lambda row: list(map(lambda e: e / parameters.NORM_FLOW, row)), flowdata))
        speeddata = list(map(lambda row: list(map(lambda e: e / parameters.NORM_SPEED, row)), speeddata))

    traffic_image = [list(map(data_input.stack_lists, flowdata, speeddata))]
    predict_data = np.array(traffic_image, dtype=np.float32)

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": predict_data},
        shuffle=False)
    predict_results_5 = model_classifier_5.predict(input_fn=predict_input_fn)

    for minute in predict_results_5:
        congestion_prob_5 = minute.get("probabilities")[1]

    predict_results_15 = model_classifier_15.predict(input_fn=predict_input_fn)

    for minute in predict_results_15:
        congestion_prob_15 = minute.get("probabilities")[1]

    predict_results_30 = model_classifier_30.predict(input_fn=predict_input_fn)

    for minute in predict_results_30:
        congestion_prob_30 = minute.get("probabilities")[1]

    return [congestion_prob_5, congestion_prob_15, congestion_prob_30]
