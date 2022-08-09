from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

import Database_connection
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')



def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


users = {'john@doe.com': '$2b$12$/TYFvXOy9wDQUOn5SKgTzedwiqB6cm.UIfPewBnz0kUQeK9Eu4mSC'}
admin_users = {'juhaszszabolcs90', 'juhasz'}


#QUESTIONS


@Database_connection.connection_handler
def get_five_latest_questions(cursor):
    query = """
        SELECT
            id,
            submission_time AS date,
            view_number AS views,
            vote_number As votes,
            title,
            message,
            image
        FROM question ORDER BY submission_time DESC LIMIT 5;
    """
    cursor.execute(query)
    return cursor.fetchall()


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


# @Database_connection.connection_handler
# def get_columns(cursor):
#     query = """
#         SELECT submission_time AS date, view_number AS views, vote_number AS votes, title, message
#         FROM question;
#     """
#     cursor.execute(query)
#     return cursor.fetchone()


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
def list_users(cursor):
    query = """
    SELECT *
    FROM users_data
    """
    cursor.execute(query)
    return cursor.fetchall()

@Database_connection.connection_handler
def get_user(cursor, user_name):
    query = """
    SELECT user_name, password
    FROM users_data
    WHERE user_name = %(user_name)s

    """
    cursor.execute(query,{'user_name': user_name})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_user(cursor, user_name):
    query = """
    SELECT id, user_name, email, password, honor, role, registration_time
    FROM users_data
    WHERE user_name = %(user_name)s
    """
    cursor.execute(query,{'user_name': user_name})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_question_by_title(cursor, title):
    query = f"""
        SELECT *
        FROM question
        WHERE title = '{title}'
        """
    cursor.execute(query)
    return cursor.fetchone()


@Database_connection.connection_handler
def add_question(cursor, user_id, title, message, image):
    dt = datetime.now()
    query = """
            INSERT INTO question(user_id, title, submission_time, message, view_number, vote_number, image)
            VALUES
            (%(user_id)s, %(title)s, %(dt)s, %(message)s, 0, 0, %(image)s)
            RETURNING id
            """
    cursor.execute(query, {'title': title, 'dt': dt, 'message': message, 'image': image, 'user_id': user_id})
    return cursor.fetchone()

@Database_connection.connection_handler
def add_users(cursor, user_name, email, password):
    dt = datetime.now()
    query = """
            INSERT INTO users_data(user_name, email, password, honor, role, registration_time)  
            VALUES
            (%(user_name)s,%(email)s,%(password)s, 0, 0, %(dt)s)
            RETURNING id
            """
    cursor.execute(query, {'user_name': user_name, 'email': email, 'password':password, 'dt': dt})
    return cursor.fetchone()


@Database_connection.connection_handler
def delete_question(cursor, id):
    query = f"""
        DELETE FROM question
        WHERE id = %(id)s
        """
    cursor.execute(query, {'id': id})


@Database_connection.connection_handler
def delete_empty_questions(cursor):
    query = """
        DELETE FROM question
        WHERE message = '';
    """
    cursor.execute(query)


@Database_connection.connection_handler
def update_question(cursor, id, title, message, image):
    query = f"""
        UPDATE question
        SET title = %(title)s,
            message = %(message)s,
            image = %(image)s
        WHERE id = %(id)s;
        """
    cursor.execute(query, {'id': id, 'title': title, 'message': message, 'image': image})


@Database_connection.connection_handler
def update_question_with_time(cursor, id, title, message, image):
    submission_time = datetime.now()
    query = f"""
        UPDATE question
        SET title = %(title)s,
            submission_time = submission_time,
            message = %(message)s,
            image = %(image)s
        WHERE id = %(id)s;
        """
    cursor.execute(query, {'id': id, 'title': title, 'submission_time': submission_time, 'message': message, 'image': image})


@Database_connection.connection_handler
def update_question_view_number(cursor, id):
    query = """
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id})


# ANSWERS


@Database_connection.connection_handler
def get_answer(cursor, id):
    query = """
        SELECT * FROM answer WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()



@Database_connection.connection_handler
def get_answers_comment_by_question_id(cursor, id):
    query = """
        SELECT answer.id AS answer_id,  comment.id, comment.message, comment.submission_time, comment.edited_count
        FROM answer 
        INNER JOIN comment ON answer.id = comment.answer_id 
        WHERE answer.question_id = %(id)s 
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@Database_connection.connection_handler
def get_answers_to_question(cursor, question_id):
    query = """
        SELECT * FROM answer WHERE question_id = %(question_id)s ORDER BY submission_time DESC;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@Database_connection.connection_handler
def add_answer(cursor, user_id, message, question_id):
    query = """
            INSERT INTO answer(submission_time, user_id, vote_number, message, question_id)
             VALUES
            (%(dt)s, %(user_id)s, 0, %(message)s, %(question_id)s)
            RETURNING id
            """
    cursor.execute(query, {'dt': datetime.now(), 'user_id': user_id, 'message': message, 'question_id': question_id})
    return cursor.fetchone()


@Database_connection.connection_handler
def delete_answer(cursor, id):
    query = """
        DELETE FROM answer
        WHERE id = %(id)s;"""
    cursor.execute(query, {'id': id})


@Database_connection.connection_handler
def edit_answer(cursor, id, message):
    query = """
        UPDATE answer
        SET message = %(message)s
        WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id, 'message': message})

# COMMENTS


@Database_connection.connection_handler
def add_comment(cursor, question_id, message):
    query = """
                INSERT INTO comment(question_id, message, submission_time, edited_count)
                 VALUES
                (%(question_id)s,%(message)s,%(dt)s,0)
                RETURNING id    
                """
    cursor.execute(query, {'question_id': question_id, 'message': message,'dt': datetime.now()})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_comment(cursor, id):
    query = """
        SELECT * FROM comment WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@Database_connection.connection_handler
def add_comment_to_answer(cursor, answer_id, message):
    query = """
                INSERT INTO comment(answer_id, message, submission_time, edited_count)
                 VALUES
                (%(answer_id)s,%(message)s,%(dt)s,0)
                RETURNING id    
                """
    cursor.execute(query, {'answer_id': answer_id, 'message': message,'dt': datetime.now()})
    return cursor.fetchone()


@Database_connection.connection_handler
def display_comment(cursor):
    query = """
            SELECT message, submission_time, edited_count
            FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@Database_connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s
        """
    cursor.execute(query, {'comment_id': comment_id})


@Database_connection.connection_handler
def add_comment(cursor, question_id, message):
    query = """
                INSERT INTO comment(question_id, message, submission_time, edited_count)
                 VALUES
                (%(question_id)s,%(message)s,%(dt)s,0)
                RETURNING id
                """
    print(question_id)
    cursor.execute(query, {'question_id': question_id, 'message': message,'dt': datetime.now()})


@Database_connection.connection_handler
def display_comment(cursor):
    query = """
            SELECT message, submission_time, edited_count
            FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@Database_connection.connection_handler
def add_comment_to_answer(cursor, answer_id, message):
    query = """
                INSERT INTO comment(answer_id, message, submission_time, edited_count)
                 VALUES
                (%(answer_id)s,%(message)s,%(dt)s,0)
                RETURNING id    
                """
    cursor.execute(query, {'answer_id': answer_id, 'message': message,'dt': datetime.now()})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_comments_about_question(cursor, question_id):
    query = """
            SELECT *
            FROM comment
            WHERE question_id = %(question_id)s;
        """
    cursor.execute(query, {'question_id':question_id})
    return cursor.fetchall()


@Database_connection.connection_handler
def update_comment_question(cursor, id, message):
    query = """
        UPDATE comment
        SET message = %(message)s
        WHERE id = %(id)s;
        """
    cursor.execute(query, {'id': id, 'message': message})


@Database_connection.connection_handler
def update_edit_count_to_comment(cursor, id):
    query = """
        UPDATE comment SET edited_count = edited_count + 1 WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id})

# VOTE


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
        WHERE id = %(id)s AND vote_number > 0;"""
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
        WHERE id = %(id)s AND vote_number > 0;"""
    cursor.execute(query, {'id': id})


# TAGS


@Database_connection.connection_handler
def add_tag(cursor, name):
    query = """
        INSERT INTO tag (name) VALUES (%(name)s)
        RETURNING id;
    """
    cursor.execute(query, {'name': name})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_tag(cursor, name):
    query = """
        SELECT id FROM tag WHERE name = %(name)s;
    """
    cursor.execute(query, {'name': name})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_tags(cursor, question_id):
    query = """
        SELECT id, name FROM tag JOIN question_tag on tag.id = question_tag.tag_id
        WHERE question_id = %(question_id)s;
    """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@Database_connection.connection_handler
def add_question_tag(cursor, question_id, tag_id):
    query = f"""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES ({question_id}, {tag_id});
    """
    cursor.execute(query)


@Database_connection.connection_handler
def get_question_id_for_tag(cursor, tag_id):
    query = f"""
        SELECT question_id FROM question_tag
        WHERE tag_id = {tag_id};
    """
    cursor.execute(query)
    return cursor.fetchone()


@Database_connection.connection_handler
def delete_tag(cursor, id):
    query = """
        DELETE FROM tag WHERE id = %(id)s;
    """
    cursor.execute(query, {'id': id})


# SEARCH

@Database_connection.connection_handler
def search(cursor, phrase):
    query = """
        SELECT DISTINCT question.id, question.title, question.message FROM question
        LEFT JOIN answer ON question.id = answer.question_id
        WHERE 
            question.title ILIKE '%%' || %(phrase)s || '%%' OR
            question.message ILIKE '%%' || %(phrase)s || '%%' OR
            answer.message ILIKE '%%' || %(phrase)s || '%%';
    """
    cursor.execute(query, {'phrase': phrase})
    return cursor.fetchall()

