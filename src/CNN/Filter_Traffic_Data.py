import gzip
import re
import parameters
import pickle


def open_and_filter_live_zipped_data(zip_path, stations_path):
    with gzip.open(zip_path, 'rb') as f:
        xml_string = f.read()
    with open(stations_path, 'r') as f:
        stations = f.readlines()
        stations = [line.strip() for line in stations]
    xml = str(xml_string).replace(">", ">\n").split("\n")

    results = []
    stationName = ''
    recording = False
    speedCount = 0
    speedSum = 0
    flowCount = 0
    flowSum = 0

    for line in xml:
        if '<measurementSiteReference' in line:
            name = re.search('id=".*" v', line)
            name = name[0][4:-3]
            if name in stations:
                recording = True
                stationName = name
        elif '</siteMeasurements>' in line and recording:
            speed = speedSum / speedCount if speedCount != 0 else -1
            flow = flowSum / flowCount if flowCount != 0 else -1
            results.append([stationName, speed, flow])
            recording = False
            speedCount = 0
            speedSum = 0
            flowCount = 0
            flowSum = 0
        else:
            if recording:
                if '</speed>' in line:
                    line = line.split('<')
                    value = float(line[0])
                    if value != -1:
                        speedCount += 1
                        speedSum += value
                elif '</vehicleFlowRate>' in line:
                    line = line.split('<')
                    value = float(line[0])
                    if value != -1:
                        flowCount += 1
                        flowSum += value
    return results


def save_pickled_window(new_data):
    filename = parameters.ROOT_DIR + '/tmp/window.pickle'
    try:
        with open(filename, 'rb') as f:
            window = pickle.load(f)
    except FileNotFoundError:
        window = []
    window.append(new_data)
    if len(window) > parameters.HISTORY:
        window.pop(0)
    with open(filename, 'wb') as f:
        pickle.dump(window, f, pickle.HIGHEST_PROTOCOL)


def format_window():
    filename = parameters.ROOT_DIR + '/tmp/window.pickle'
    speeddata = []
    flowdata = []
    with open(filename, 'rb') as f:
        window = pickle.load(f)
    if len(window) == parameters.HISTORY:
        for i in range(len(window[0])):
            name = window[0][i][0]
            speeddata.append([name])
            flowdata.append([name])
            for j in range(len(window)):
                speeddata[i].append(window[j][i][1])
                flowdata[i].append(window[j][i][2])
    else:
        raise IndexError("Window length insufficient")
    return speeddata, flowdata
