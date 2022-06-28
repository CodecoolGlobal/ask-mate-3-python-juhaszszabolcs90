import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'user_history.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def read_data(filename):
    with open(filename, newline='') as questions:
    return list(csv.DictReader(questions, delimiter=","))


def write_data(filename, data):
    with open('filename', 'a', newline='') as f:
        writer = csv.DictWriter(f, DATA_HEADER)
        writer.writerows(data)




