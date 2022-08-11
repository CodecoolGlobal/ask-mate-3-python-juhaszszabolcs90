import data_manager
from flask import request


def get_ordered_questions(column_names):
    for_order_by = request.args.get('sort', 'title|ASC').split('|')
    order_by = for_order_by[0]
    order = for_order_by[1]

    return data_manager.get_and_sort_questions(column_names[order_by], order)


def get_question_information(question_id):
    return {
        'question': data_manager.get_question(question_id),
        'answers': data_manager.get_answers_to_question(data_manager.get_question(question_id).get('id')),
        'answers_comment': data_manager.get_answers_comment_by_question_id(data_manager.get_question(question_id).get('id')),
        'comment_messages': data_manager.get_comments_about_question(question_id),
        'tags': data_manager.get_tags(question_id),
        'users': data_manager.list_users()
    }
