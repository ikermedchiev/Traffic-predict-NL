import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset properties
NORMALIZED = True
NORM_SPEED = 150
NORM_FLOW = 5000
HISTORY = 30
FUTURE = 5

# Training properties
BATCHSIZE = 128
LEARNINGRATE = 0.00001
STEPS = 200000

# Realtime properties
REALTIMEDATA = "http://opendata.ndw.nu/trafficspeed.xml.gz"
