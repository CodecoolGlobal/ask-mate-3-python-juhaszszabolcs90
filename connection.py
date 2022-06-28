import csv

DATA_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def read_questions() ->list:
    with open('sample_data/question.csv', newline='') as questions:
        questions = list(csv.DictReader(questions, delimiter=","))
    return questions