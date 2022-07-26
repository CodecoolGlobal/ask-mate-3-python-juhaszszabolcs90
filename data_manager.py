from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import Database_connection


@Database_connection.connection_handler
def get_questions(cursor):
    query = """
        SELECT
        id,
        submission_time AS date,
        view_number AS views,
        vote_number As votes,
        title,
        message,
        image
        FROM question
        ORDER BY submission_time DESC;"""
    cursor.execute(query)
    return cursor.fetchall()


@Database_connection.connection_handler
def get_columns(cursor):
    query = """
        SELECT submission_time AS date, view_number AS views, vote_number AS votes, title, message
        FROM question;
    """
    cursor.execute(query)
    return cursor.fetchone()


@Database_connection.connection_handler
def get_answer(cursor, answer_id):
    query = """
        SELECT * FROM answer WHERE answer_id = %(answer_id)s;
    """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@Database_connection.connection_handler
def sort_questions(cursor, order_by, order):
    if order in ['ASC', 'DESC']:
        query = sql.SQL("""
            SELECT
            id,
            submission_time AS date,
            view_number AS views,
            vote_number As votes,
            title,
            message,
            image
            FROM question
            ORDER BY {order_by} {order};""").format(order_by=sql.Identifier(order_by), order=sql.SQL(order))
    else:
        raise Exception('Order is not one of values ASC/DESC')
    cursor.execute(query)
    return cursor.fetchall()


@Database_connection.connection_handler
def vote_answer_up(cursor, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id})


@Database_connection.connection_handler
def vote_answer_down(cursor, answer_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id})


@Database_connection.connection_handler
def vote_question_up(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(queston_id)s;"""
    cursor.execute(query, {'question_id': question_id})


@Database_connection.connection_handler
def vote_question_down(cursor, question_id):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(queston_id)s;"""
    cursor.execute(query, {'question_id': question_id})


@Database_connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id})


@Database_connection.connection_handler
def delete_question(cursor, question_id):
    query = f"""
        DELETE FROM question
        WHERE id = '{question_id}'
        """
    cursor.execute(query)
    return "Succesfully deleted"
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
