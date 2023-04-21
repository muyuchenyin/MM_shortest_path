import json
import os
import datetime

start_time = datetime.datetime(2008, 2, 3, 13, 32, 3)
time_list = []


def init_timelist():
    tmp_time = start_time
    time_list.append(start_time)
    for i in range(1, 10000):
        tmp_time = tmp_time + datetime.timedelta(minutes=1)
        time_list.append(tmp_time)
    # print(list(time_list))


def load():
    with open("./data/train_traj.json") as f:
        data_traj = json.load(f)

    for i in data_traj:
        s = str(i) + ".txt"
        filename = os.path.join('data', 'trajdata_row', s)
        # time = "2008/02/03 13:32:03"
        # tmp_str = "#," + time + "," + str(i) + ",2008/02/05 11:08:34,2008/02/05 11:18:34,1.3397859980572806 km"
        with open(filename, 'w') as f:
            num = 0
            for x in data_traj[i][1]:
                tmp = time_list[num]
                num = num + 1
                f.write('{},{},{},{}\n'.format(i, tmp, x[0], x[1]))
        f.close()


if __name__ == '__main__':
    # print(start_time)
    init_timelist()
    load()
