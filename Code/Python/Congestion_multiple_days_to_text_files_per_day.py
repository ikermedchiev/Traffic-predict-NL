from _datetime import datetime
import datetime as dt

class File():
    def __init__(self, param_list):
        self.start_pos = float(param_list[0])
        self.end_pos = float(param_list[1])
        self.start_time = File._string2time(param_list[2], param_list[4])
        self.end_time = File._string2time(param_list[3], param_list[4])

    @staticmethod
    def _string2time(timestring, datestring):
        [hour, minute] = list(map(int, timestring.split(':')[:2]))
        [month, day, year] = list(map(int, datestring.split('/')))
        if "PM" in timestring:
            hour += 12
        return dt.datetime(year, month, day, hour, minute)

    def __str__(self):
        return "Position: " + str(self.start_pos) + " - " + str(self.end_pos)+\
               "\tTime: " + str(self.start_time) + " - " + str(self.end_time)

with open("Files_A4.txt") as f:
    content = f.readlines()
content = [File(x.strip().split(',')) for x in content]

print(content)
print(len(content))

content.sort(key=lambda x: x.start_time)

start_time = dt.time(6)
current_date = content[0].start_time.date()

is_file = [0]*900

for file in content:
    while file.start_time.date() != current_date:
        #Write to text file
        bestand = open(str(current_date) + ".txt", "w")
        bestand.write(",".join([str(x) for x in is_file]))
        bestand.close()
        print("File " + str(current_date) + ".txt written successfully")
        is_file = [0]*900
        current_date += dt.timedelta(days=1)

    start_index = (file.start_time - datetime.combine(current_date, start_time)).total_seconds()/60
    end_index = (file.end_time - datetime.combine(current_date, start_time)).total_seconds()/60
    is_file[int(start_index):int(end_index) + 1] = [1] * int(end_index - start_index + 1)

bestand = open(str(current_date) + ".txt", "w")
bestand.write(",".join([str(x) for x in is_file]))
bestand.close()
print("File " + str(current_date) + ".txt written successfully")


