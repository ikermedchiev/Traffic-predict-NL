from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Imports
import tensorflow as tf
import math
import data_input
import pickle
import parameters

tf.logging.set_verbosity(tf.logging.INFO)


def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""
    # Input Layer
    input_layer = tf.reshape(features["x"], [-1, 49, parameters.HISTORY, 2])

    # Convolutional Layer #1
    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=32,
        kernel_size=[7, 20],
        padding="same",
        activation=tf.nn.relu)

    # Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    # Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Dense Layer
    pool2_flat = tf.reshape(pool2, [-1, 12 * math.floor(parameters.HISTORY/4) * 64])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=2)

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=parameters.LEARNINGRATE)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(labels=labels, predictions=predictions["classes"])
    }
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


def main(unused_argv):
    # Load training and eval data
    print('Start main')
    train_data, train_labels, eval_data, eval_labels = load_data()

    # Create the Estimator
    print('Create estimator')
    model_classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir=parameters.ROOT_DIR +
                                                                                        '/tmp/bsize_' +
                                                                                        str(parameters.BATCHSIZE) +
                                                                                        '_hist_' +
                                                                                        str(parameters.HISTORY) +
                                                                                        '_futr_' +
                                                                                        str(parameters.FUTURE) +
                                                                                        '_lr_' +
                                                                                        str(parameters.LEARNINGRATE))

    # Set up logging for predictions
    print('Set up logger')
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    # Train the model
    print('Train model')
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_labels,
        batch_size=parameters.BATCHSIZE,
        num_epochs=None,
        shuffle=True)
    model_classifier.train(
        input_fn=train_input_fn,
        steps=parameters.STEPS,
        hooks=[logging_hook])

    # Evaluate the model and print results
    print('Evaluate model')
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = model_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)


def data_import():
    train_img_list = []
    eval_img_list = []
    counter = [0, 0]
    for day in range(14, 22):
        for minute in range(parameters.HISTORY, 900):
            img = data_input.image_object(2018, 3, day, minute, parameters.HISTORY, parameters.FUTURE,
                                          parameters.NORMALIZED, parameters.NORM_FLOW, parameters.NORM_SPEED)
            if img.is_congestion:
                counter[1] += 1
                if counter[1] % 6:
                    # 1 out of 6 goes to eval set, 5 go to train set
                    train_img_list.append(img)
                else:
                    eval_img_list.append(img)
            else:
                counter[0] += 1
                if counter[0] % 6:
                    train_img_list.append(img)
                else:
                    eval_img_list.append(img)
            print(str(day) + ', ' + str(minute))
    return data_input.image_list_to_np_array(train_img_list), data_input.image_list_to_np_array(eval_img_list)


def store_data(filename: str):
    (train_data, train_labels), (eval_data, eval_labels) = data_import()
    data = {
        'train_data': train_data,
        'train_labels': train_labels,
        'eval_data': eval_data,
        'eval_labels': eval_labels
    }

    with open(filename, 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def load_data(filename: str = None):
    if filename is None:
        if parameters.NORMALIZED:
            filename = parameters.ROOT_DIR + '/pickled/model_data_norm_speed_' + str(parameters.NORM_SPEED) +\
                                             '_flow_' + str(parameters.NORM_FLOW) +\
                                             '_hist_' + str(parameters.HISTORY) +\
                                             '_futr_' + str(parameters.FUTURE) + '.pickle'
        else:
            filename = parameters.ROOT_DIR + '/pickled/model_data' +\
                                             '_hist_' + str(parameters.HISTORY) +\
                                             '_futr_' + str(parameters.FUTURE) + '.pickle'

    try:
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data['train_data'], data['train_labels'], data['eval_data'], data['eval_labels']
    except FileNotFoundError:
        store_data(filename)
        return load_data(filename)


if __name__ == "__main__":
    tf.app.run()
