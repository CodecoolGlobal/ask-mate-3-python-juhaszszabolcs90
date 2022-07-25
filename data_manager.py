import connection
import csv
import operator

def update_data(filename, data, headers):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        writer.writerows(data)


def delete_question(id_question):
    questions = connection.read_data('sample_data/question.csv')
    filtered_questions = filter(lambda question: question['id'] != id_question, questions)
    connection.write_data('sample_data/question.csv', list(filtered_questions))


def should_delete_question(id_question):
    questions = connection.read_data('sample_data/question.csv')


def sort_data(data, sort_by='submission_time', reverse=False):
    # for d in data:
    #     try:
    #         for k, v in d.items():
    #             d[k] = int(v)
    #     except ValueError:
    #         for k, v in d.items():
    #             d[k] = str(v).lower()
    # print(data)
    return sorted(data, key=operator.itemgetter(sort_by), reverse=reverse)

def delete_answer(id_answer):
    answers = connection.read_data('sample_data/answer.csv')
    filtered_answers = filter(lambda answer: answer['id'] != id_answer, answers)
    connection.write_data('sample_data/answer.csv', list(filtered_answers))
