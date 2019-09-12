from urllib.request import urlopen
import parameters

def zip_pull():
    resp = urlopen(parameters.REALTIMEDATA)
    return resp
