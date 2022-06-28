import csv
import os

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'user_history.csv'


def read_questions():
    with open('filename', newline='' ) as questions:
        questions = list(csv.DictReader(questions, delimiter=","))
    return questions

def write_questions():
    with open('filename','w', newline='') as answers:
        answers = list(csv.DictReader(answers, delimiter=","))
    return answers
