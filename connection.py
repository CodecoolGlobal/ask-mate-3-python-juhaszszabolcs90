import csv

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def read_data(filename):
    with open(filename, newline='') as questions:
    return list(csv.DictReader(questions, delimiter=","))


def write_data(filename, data):
    with open(filename, 'a', newline='') as writer:
        writer = csv.DictWriter(writer, DATA_HEADER)
        writer.writerows(data)
