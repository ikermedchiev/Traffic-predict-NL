import sched
import time
import file_pull
import Filter_Traffic_Data
import parameters
import predict_picture


def run_app(sc, call_time, filename):
    # Schedule next run
    next_call_time = call_time + 60
    sc.enterabs(next_call_time, 1, run_app, (sc, next_call_time, filename))
    print("Run started at: " + time.asctime(time.gmtime()) + ", next run scheduled at " +
          time.asctime(time.gmtime(next_call_time)))

    # Download data
    try:
        file = file_pull.zip_pull()
        print("Data successfully downloaded from: " + parameters.REALTIMEDATA)
    except Exception as e:
        print("Exception occurred during data download!")
        raise e

    # Process data
    try:
        results = Filter_Traffic_Data.open_and_filter_live_zipped_data(file,
                                                                       parameters.ROOT_DIR +
                                                                       "/data/measurementSiteIDs.txt")
        print("Data successfully filtered.")
    except Exception as e:
        print("Exception occurred during unpacking and filtering!")
        raise e

    # Add new data to sliding window
    try:
        Filter_Traffic_Data.save_pickled_window(results)
        print("New result successfully added to window.")
    except Exception as e:
        print("Exception occurred during adding data to window!")
        raise e

    try:
        speeddata, flowdata = Filter_Traffic_Data.format_window()
        # Perform prediction
        congestion_prob = predict_picture.main(flowdata, speeddata)
        for i in range(3):
            with open(filename[i], 'a') as file:
                file.write(time.asctime(time.gmtime(call_time)) + " : " + str(congestion_prob[i]) + "\n")

    except IndexError:
        print("Window length isn't sufficient yet!")

    print("------------------------------------------------------------------------------")


# Set up initial scheduler call
s = sched.scheduler(time.time, time.sleep)
current_time = time.time()
dtime = current_time % 60
next_call_time = current_time + 60 - dtime

# Create output file
start_time = time.gmtime(next_call_time)
result_file = parameters.ROOT_DIR + "/results/realtime"
result_files = [result_file + "_5.txt", result_file + "_15.txt", result_file + "_30.txt"]

for i in range(3):
    with open(result_files[i], 'w') as f:
        pass

# Start execution
s.enterabs(next_call_time, 1, run_app, (s, next_call_time, result_files))
s.run()
