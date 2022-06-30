import connection
import csv

import server


def update_user_story(filename):

    with open(filename, 'w', newline='') as datas:
        writer = csv.DictWriter(datas,)
        writer.writeheader()
        writer.writerows(row)


def delete_question(id_question):
    questions = connection.read_data('sample_data/question.csv')
    filtered_questions = filter(lambda question: question['id'] != id_question, questions)
    connection.write_data('sample_data/question.csv', list(filtered_questions))


def should_delete_question(id_question):
    questions = connection.read_data('sample_data/question.csv')


def delete_answer(id_answer):
    answers = connection.read_data('sample_data/answer.csv')
    filtered_answers = filter(lambda answer: answer['id'] != id_answer, answers)
    connection.write_data('sample_data/answer.csv', list(filtered_answers))
