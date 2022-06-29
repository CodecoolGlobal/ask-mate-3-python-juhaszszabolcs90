import connection
import datetime


def generate_id(filename):
    datas = connection.read_data(filename)
    id = max([int(data['id']) for data in datas]) + 1
    return str(id)

def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y %B, %d")

def generate_timestamp():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

def vote(up, filename):
    datas = connection.read_data(filename)

    for data in datas:
        if data['id'] == id:
            if not up and int(data['id']) > 0:
                vote_num = int(datas[data['vote_number']])
                vote_num -= 1
                datas[data['vote_number']] = str(vote_num)
            else:
                vote_num = int(datas[data['vote_number']])
                vote_num += 1
                datas[data['vote_number']] = str(vote_num)

    data_manager.update_data(datas)