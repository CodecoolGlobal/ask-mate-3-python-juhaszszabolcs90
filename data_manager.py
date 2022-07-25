from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import Database_connection

@Database_connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT
        submission_time AS date,
        view_number AS views,
        vote_number As votes,
        title,
        message,
        image
        FROM question;"""
    cursor.execute(query)
    return cursor.fetchall()

# select // from question DISPLAY QUESTIONS
# select // from question where id join answer question id question id
# insert into question ADD Q
# select id from question order by id desc limit 1 ADD QUESTION
# DELETE from question WHERE question_id LIKE '%{delete_id}%'
# UPDATE question SET question = '{updated_question}' WHERE question_id = '{question_id}'


# @Database_connection.connection_handler
# def get_question(cursor)
#query = """
        #SELECT

# cursor.execute(query
# #return cursor.fetchone()


# def update_data(filename, data, headers):
#     with open(filename, 'w', newline='') as f:
#
#
#
# def delete_question(id_question):
#     questions = connection.read_data('sample_data/question.csv')
#     filtered_questions = filter(lambda question: question['id'] != id_question, questions)
#     connection.write_data('sample_data/question.csv', list(filtered_questions))
#
#
# def should_delete_question(id_question):
#     questions = connection.read_data('sample_data/question.csv')
#
#
# def sort_data(data, sort_by='submission_time', reverse=False):
#     # for d in data:
#     #     try:
#     #         for k, v in d.items():
#     #             d[k] = int(v)
#     #     except ValueError:
#     #         for k, v in d.items():
#     #             d[k] = str(v).lower()
#     # print(data)
#     return sorted(data, key=operator.itemgetter(sort_by), reverse=reverse)
#
# def delete_answer(id_answer):
#     answers = connection.read_data('sample_data/answer.csv')
#     filtered_answers = filter(lambda answer: answer['id'] != id_answer, answers)
#     connection.write_data('sample_data/answer.csv', list(filtered_answers))
