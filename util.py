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