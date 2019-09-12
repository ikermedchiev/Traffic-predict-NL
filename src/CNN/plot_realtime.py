import parameters
from datetime import datetime, timedelta
import matplotlib.dates
import matplotlib.pyplot as plt


def obtain_prediction_data(future):
    result_file = parameters.ROOT_DIR + "/results/realtime_" + str(future) + ".txt"

    datelist = []
    problist = []
    with open(result_file, 'r') as file:
        lines = file.readlines()

    lines = [line.strip().split(' : ') for line in lines]
    # Remove leading empty lines
    while lines[0][0] == '':
        lines.pop(0)

    for line in lines:
        datetime_object = datetime.strptime(line[0], '%a %b %d %H:%M:%S %Y')
        datelist.append(datetime_object + timedelta(minutes=future))
        problist.append(float(line[1]))

    return datelist, problist


def add_to_dateplot(datelist, problist, ax, format, lbl):
    dates = matplotlib.dates.date2num(datelist)
    ax.plot_date(dates, problist, fmt=format, label=lbl)


fig, ax = plt.subplots(figsize=(15, 5))
future_times = [5, 15, 30]
formats = ['b-', 'g-', 'r-']
labels = ['5 min ahead', '15 min ahead', '30 min ahead']

for i in range(3):
    datelist, problist = obtain_prediction_data(future_times[i])
    add_to_dateplot(datelist, problist, ax, formats[i], labels[i])

ax.set_ylim(0, 1.1)
ax.set_ylabel("Congestion probability")
ax.set_xlabel("Predicted time (UTC)")  # Offset is included in the plot

minutes = matplotlib.dates.MinuteLocator(interval=5)
hours = matplotlib.dates.HourLocator()
hoursFmt = matplotlib.dates.DateFormatter('%d %b %H:%M')

ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)
ax.xaxis.set_minor_locator(minutes)

ax.grid(True)
fig.autofmt_xdate()
ax.legend()

# plt.show()
plt.savefig(parameters.ROOT_DIR + "/results/figures/realtime_results.png")
