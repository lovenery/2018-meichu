import json
import dateutil.parser
import datetime
# import threading

# https://stackoverflow.com/questions/969285/how-do-i-translate-an-iso-8601-datetime-string-into-a-python-datetime-object/18942106#comment65884904_3908349
# s = '2018-02-21T02:32:56.190Z'
# date = dateutil.parser.parse(s)
# print(s)
# print(date.year, date.month, date.day, date.hour)

from os import path
from glob import glob

def load_files():
    base_dir = path.abspath(path.dirname(__file__))
    relative_path = 'brise'
    regex_full_path = path.join(base_dir, relative_path + "/*")

    file_names = glob(regex_full_path)
    return file_names

def write_to_csv(input_file_path, base_name):
    file_name = input_file_path
    new_file_name = 'output/{}.csv'.format(base_name)
    with open(new_file_name, 'w') as f:
            f.write('date,timestamp,pm2.5,temperature,humidity,filter\n')
    
    with open(file_name) as f:
        with open(new_file_name, 'a') as new_f:
            now_date = datetime.datetime.now()
            pm25_total = 0
            pm25_counter = 0
            temperature_total = 0
            temperature_counter = 0
            humidity_total = 0
            humidity_conunter = 0
            filter_total = 0
            filter_counter = 0
            for index, line in enumerate(f):
                # print('Line {}: {}'.format(index, line))
                data = json.loads(line)
                time = data['time']['$date']
                sid = data['sid']
                value = data['value']
                value_str = list(value)[0]

                datetime_obj = dateutil.parser.parse(time)
                new_time = '{}-{:02}-{:02}T{:02}'.format(datetime_obj.year, datetime_obj.month, datetime_obj.day, datetime_obj.hour)

                # if (sid != 'pm2.5'):
                #     continue

                if (new_time != now_date):
                    # if (pm25_counter > 0):
                    #     print('{} {} {:.2f}'.format(new_time, 'pm2.5', pm25_total/pm25_counter))
                    # if (temperature_counter > 0):
                    #     print('{} {} {:.2f}'.format(new_time, 'temperature', temperature_total/temperature_counter))
                    # if (humidity_conunter > 0):
                    #     print('{} {} {:.2f}'.format(new_time, 'humidity', humidity_total/humidity_conunter))
                    # if (filter_counter > 0):
                    #     print('{} {} {:.2f}'.format(new_time, 'filter', filter_total/filter_counter))

                    datetime_obj = dateutil.parser.parse(time)
                    new_datetime = datetime.datetime(datetime_obj.year, datetime_obj.month, datetime_obj.day, datetime_obj.hour)
                    if (pm25_counter > 0 and temperature_counter > 0 and humidity_conunter > 0 and filter_counter > 0):
                        result = '{},{:.0f},{:.2f},{:.2f},{:.2f},{:.2f}'.format(new_time, new_datetime.timestamp(),
                            pm25_total/pm25_counter, 
                            temperature_total/temperature_counter, 
                            humidity_total/humidity_conunter, 
                            filter_total/filter_counter
                        )
                        new_f.write(result + '\n')
                        # print(result)

                    pm25_total = 0
                    pm25_counter = 0
                    temperature_total = 0
                    temperature_counter = 0
                    humidity_total = 0
                    humidity_conunter = 0
                    filter_total = 0
                    filter_counter = 0

                    now_date = new_time
                else:
                    if (sid == 'pm2.5'):
                        pm25_total += int(value_str)
                        pm25_counter += 1

                    if (sid == 'temperature'):
                        temperature_total += int(value_str)
                        temperature_counter += 1

                    if (sid == 'humidity'):
                        humidity_total += int(value_str)
                        humidity_conunter += 1

                    if (sid == 'filter'):
                        filter_total += int(value_str)
                        filter_counter += 1

file_names = load_files()
# threads = []
for f in file_names:
    write_to_csv(f, path.basename(f))

    # t = threading.Thread(target=write_to_csv, args=(f, path.basename(f)))
    # threads.append(t)
    # t.start()

# write_to_csv('brise/0694317100256465', '0694317100256465')