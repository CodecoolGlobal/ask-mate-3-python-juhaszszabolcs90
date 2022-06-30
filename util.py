import connection
import datetime


headers = connection.DATA_HEADER

def generate_id(filename):
    datas = connection.read_data(filename)
    id = max([int(data['id']) for data in datas]) + 1
    return str(id)

def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y %B, %d")

def generate_timestamp():
    return datetime.datetime.timestamp(datetime.datetime.now())

def vote(filename, up=True):
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


def convert_headers(headers):
    return [header.upper().replace('_', ' ') for header in headers]
