import csv
import os

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER= ['Id', 'Submission time', 'Vote number', 'Question Id', 'Message', 'Image']


def read_data(filename):
    with open(filename, newline='') as questions:
        questions = list(csv.DictReader(questions, delimiter=","))
    return questions


def append_data(filename, data: dict):
    with open(filename, 'a', newline='') as datas:
        writer = csv.DictWriter(datas, data.keys())
        writer.writerow(data)

def write_data(filename, data : list):
    with open(filename, "w", newline='') as write:
        if len(data) == 0:
            return
        writer = csv.DictWriter(write, data[0].keys())
        writer.writeheader()
        writer.writerows(data)
