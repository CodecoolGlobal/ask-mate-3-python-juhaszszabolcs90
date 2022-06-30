import connection
import csv


def update_data(filename, data):

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, connection.DATA_HEADER)
        writer.writeheader()
        writer.writerows(data)


def delete_question(id_question):
    questions = connection.read_data('sample_data/question.csv')
    filtered_questions = filter(lambda question: question['id'] != id_question, questions)
    connection.write_data('sample_data/question.csv', list(filtered_questions))


def should_delete_question(id_question):
    questions = connection.read_data('sample_data/question.csv')



