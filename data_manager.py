from psycopg2 import sql
from datetime import datetime

import Database_connection

# USERS


@Database_connection.connection_handler
def list_users(cursor):
    query = """
        SELECT users_data.*,
            COUNT(DISTINCT q.id) AS number_of_questions,
            COUNT(DISTINCT a.id) AS number_of_answers,
            COUNT(DISTINCT c.id) AS number_of_comments
            FROM users_data 
        LEFT JOIN question q on  q.user_id =users_data.id
        LEFT JOIN answer a on a.user_id = users_data.id
        LEFT JOIN comment c on c.user_id = users_data.id 
        GROUP BY users_data.id
    """
    cursor.execute(query)
    return cursor.fetchall()

@Database_connection.connection_handler
def list_tags(cursor):
    query = """
        SELECT tag.name, COUNT(tag_id) AS amount_of_tags
        FROM tag
            inner join question_tag qt on tag.id = qt.tag_id
        GROUP BY tag.name
    """
    cursor.execute(query)
    return cursor.fetchall()

@Database_connection.connection_handler
def get_user_answer_list(cursor, user_name):
    query = """
    SELECT answer.message, answer.id, question_id
    FROM answer
        left join users_data ud on ud.id = answer.user_id
    WHERE user_name = %(user_name)s
    GROUP BY answer.message, answer.id
    """
    cursor.execute(query, {'user_name': user_name})
    return cursor.fetchall()


@Database_connection.connection_handler
def get_user_question_list(cursor, user_name):
    query = """
    SELECT question.title,question.id
    FROM question
        left join users_data ud on ud.id = question.user_id
    WHERE user_name = %(user_name)s
    GROUP BY question.title,question.id
    """
    cursor.execute(query, {'user_name': user_name})
    return cursor.fetchall()


@Database_connection.connection_handler
def get_user_comment_list(cursor, user_name):
    query = """
    SELECT comment.message, comment.id, COALESCE(comment.question_id, a.question_id) AS question_id
    FROM comment
        left join users_data ud on ud.id = comment.user_id
        left join answer a on comment.answer_id = a.id
    WHERE user_name = %(user_name)s
    GROUP BY comment.id, a.id
    """
    cursor.execute(query, {'user_name': user_name})
    return cursor.fetchall()


@Database_connection.connection_handler
def get_user_answer_question_comment_count(cursor, user_name):
    query = """
    SELECT users_data.*,
       (SELECT COUNT(question.user_id) from question where question.user_id = users_data.id) AS number_of_questions,
       (SELECT COUNT(answer.user_id) from answer where answer.user_id = users_data.id) AS number_of_answers,
       (SELECT COUNT(comment.user_id) from comment where comment.user_id = users_data.id) AS number_of_comments FROM users_data
    WHERE user_name = %(user_name)s
    """
    cursor.execute(query, {'user_name': user_name})
    return cursor.fetchone()


@Database_connection.connection_handler
def add_users(cursor, user_name, email, password):
    dt = datetime.now()
    query = """
            INSERT INTO users_data(user_name, email, password, honor, role, submission_time)  
            VALUES
            (%(user_name)s,%(email)s,%(password)s, 0, 0, %(dt)s)
            RETURNING id
            """
    cursor.execute(query, {'user_name': user_name, 'email': email, 'password':password, 'dt': dt})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_user(cursor, user_name):
    query = """
    SELECT id, user_name, email, password, honor, role, submission_time
    FROM users_data
    WHERE user_name = %(user_name)s
    """
    cursor.execute(query,{'user_name': user_name})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_user_by_id(cursor, id):
    query = """
    SELECT id, user_name
    FROM users_data
    WHERE id = %(id)s"""
    cursor.execute(query, {'id': id})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_user_id_by_answer_id(cursor, answer_id):
    query = """
        SELECT user_id FROM answer
        WHERE id = %(answer_id)s; 
        """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@Database_connection.connection_handler
def get_user_id_by_question_id(cursor, question_id):
    query = """
        SELECT user_id FROM question
        WHERE id = %(question_id)s; 
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


# QUESTIONS


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
    cursor.execute(query, {'dt': datetime.now(), 'user_id':user_id, 'message': message, 'question_id': question_id})
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


@Database_connection.connection_handler
def accept_answer(cursor, id, acception_state):
    query = """
    UPDATE answer
    SET accepted = %(acception_state)s
    WHERE id = %(id)s;"""
    cursor.execute(query, {'id': id, 'acception_state': acception_state})

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
def add_comment(cursor, question_id, message, user_id):
    query = """
                INSERT INTO comment(question_id, user_id, message, submission_time, edited_count)
                 VALUES
                (%(question_id)s, %(user_id)s, %(message)s,%(dt)s,0)
                RETURNING id
                """
    print(question_id)
    cursor.execute(query, {'question_id': question_id, 'user_id': user_id, 'message': message,'dt': datetime.now()})


@Database_connection.connection_handler
def display_comment(cursor):
    query = """
            SELECT message, submission_time, edited_count
            FROM comment
        """
    cursor.execute(query)
    return cursor.fetchall()


@Database_connection.connection_handler
def add_comment_to_answer(cursor, user_id, answer_id, message):
    query = """
                INSERT INTO comment(user_id, answer_id, message, submission_time, edited_count)
                 VALUES
                (%(user_id)s, %(answer_id)s,%(message)s,%(dt)s,0)
                RETURNING id    
                """
    cursor.execute(query, {'user_id': user_id, 'answer_id': answer_id, 'message': message,'dt': datetime.now()})
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
def vote_answer_up(cursor, id, user_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(id)s;
        UPDATE users_data
        SET honor = honor + 10
        WHERE id = %(user_id)s;"""
    cursor.execute(query, {'id': id, 'user_id': user_id})


@Database_connection.connection_handler
def vote_answer_down(cursor, id, user_id):
    query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(id)s AND vote_number > 0;
        UPDATE users_data
        SET honor = honor - 2 
        WHERE id = %(user_id)s;"""
    cursor.execute(query, {'id': id, 'user_id': user_id})


@Database_connection.connection_handler
def vote_question_up(cursor, id, user_id):
    query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(id)s;
        UPDATE users_data
        SET honor = honor + 5
        WHERE id = %(user_id)s;"""
    cursor.execute(query, {'id': id, 'user_id': user_id})


@Database_connection.connection_handler
def vote_question_down(cursor, id, user_id):
    query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(id)s AND vote_number > 0;
        UPDATE users_data
        SET honor = honor - 2
        WHERE id = %(user_id)s;"""
    cursor.execute(query, {'id': id, 'user_id': user_id})


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
    return cursor.fetchall()\


# HONOR


@Database_connection.connection_handler
def increase_honor_by_accepted_answer(cursor, user_id):
    query = """
    UPDATE users_data 
    SET honor = honor + 15 
    WHERE id = %(user_id)s;"""
    cursor.execute(query, {'user_id': user_id})


@Database_connection.connection_handler
def decrease_honor_by_accepted_answer(cursor, user_id):
    query = """
    UPDATE users_data 
    SET honor = honor - 15 
    WHERE id = %(user_id)s;"""
    cursor.execute(query, {'user_id': user_id})
