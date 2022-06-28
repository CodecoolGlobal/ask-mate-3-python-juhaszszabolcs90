import csv
import os

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def read_questions(filename):
    with open(filename, newline='') as questions:
        questions = list(csv.DictReader(questions, delimiter=","))
    return questions


def write_questions(filename, data: dict):
    with open(filename, 'a', newline='') as datas:
        writer = csv.DictWriter(datas, DATA_HEADER)
        writer.writerow(data)
