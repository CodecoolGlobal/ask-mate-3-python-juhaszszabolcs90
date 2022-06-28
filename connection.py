import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'user_history.csv'
DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def read_questions(filename):
    with open(filename, newline='') as questions:
        questions = list(csv.DictReader(questions, delimiter=","))
    return questions


def write_questions():
    with open('filename', 'a', newline='') as writer:
        writer = csv.DictWriter(writer,DATA_HEADER)
        writer.writerows()
