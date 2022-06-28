from datetime import datetime
import connection

def generate_id(datas=connection.read_data(filename)):
    for data in datas:
        data["id"] = data["submission_time"][len(data["submission_time"])-3:]


def convert_timestamp():
    pass


def convert_datetime():
    pass