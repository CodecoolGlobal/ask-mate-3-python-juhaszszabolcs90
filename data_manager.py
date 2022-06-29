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



