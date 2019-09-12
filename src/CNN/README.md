# Source root directory

## To run the code:
- Add the following folders locally to the CNN directory:
  - pickled
  - results
  - tmp

### Installs required
- Python 3.6, 64 bit
- Packages
  - pytest
  - tensorflow
  - matplotlib

### When using a (CUDA enabled) GPU
- Packages
  - tensorflow-gpu
- Drivers (for [CUDA enabled GPU's](https://www.geforce.com/hardware/technology/cuda/supported-gpus))
  - [CUDA 9.0](https://developer.nvidia.com/cuda-90-download-archive)
  - [cuDNN 7 for CUDA 9.0](https://developer.nvidia.com/rdp/cudnn-download)

## Instructions:
1. Several parameters can be tuned in the parameters.py file.
2. Train a network by running: cnn_congestion.py
3. Generate predictions by running: cnn_predict.py
4. Generate 8 day prediction plots by running: plot_prediction.py
5. Generate the confusion matrix by running: confusion_matrix.py
6. Generate the varying threshold figure by running: optimal_threshold.py
7. Run the real time application by running: realtime_app.py (needs the specified 3 networks to be trained, can of course be changed)
