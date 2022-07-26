from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

import Database_connection


@Database_connection.connection_handler
def get_and_sort_questions(cursor, order_by='submission_time', order='DESC'):
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
def get_columns(cursor):
    query = """
        SELECT submission_time AS date, view_number AS views, vote_number AS votes, title, message
        FROM question;
    """
    cursor.execute(query)
    return cursor.fetchone()


@Database_connection.connection_handler
def get_answer(cursor, id):
    query = """
        SELECT * FROM answer WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_answers_to_question(cursor, question_id):
    query = """
        SELECT * FROM answer WHERE question_id = %(question_id)s ORDER BY submission_time DESC;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@Database_connection.connection_handler
def get_question(cursor, id):
    query = f"""
        SELECT *
        FROM question
        WHERE id = '{id}'
        """
    cursor.execute(query)
    return cursor.fetchone()


@Database_connection.connection_handler
def add_question(cursor, title, message):
    dt = datetime.now()
    query = """
            INSERT INTO question(title, submission_time, message, view_number, vote_number)
            VALUES
            (%(title)s, %(dt)s, %(message)s, 0, 0)
            RETURNING id
            """
    cursor.execute(query, {'title': title, 'dt': dt, 'message': message})
    return cursor.fetchone()


@Database_connection.connection_handler
def vote_answer_up(cursor, id):
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(id)s;"""
    cursor.execute(query, {'id': id})


@Database_connection.connection_handler
def vote_answer_down(cursor, id):
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(id)s;"""
    cursor.execute(query, {'id': id})


@Database_connection.connection_handler
def vote_question_up(cursor, id):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(id)s;"""
    cursor.execute(query, {'id': id})


@Database_connection.connection_handler
def vote_question_down(cursor, id):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(id)s;"""
    cursor.execute(query, {'id': id})


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


@Database_connection.connection_handler
def delete_comment(cursor, question_id):
    query = f"""
        DELETE FROM comment
        WHERE question_id = '{question_id}';
        """
    cursor.execute(query)


@Database_connection.connection_handler
def update_question(cursor, id, title, message):
    query = f"""
        UPDATE question
        SET title = '{title}',
            message = '{message}'
        WHERE id = '{id}';
        """
    cursor.execute(query)
