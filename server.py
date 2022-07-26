from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import data_manager

import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/images'

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/list")
def display_questions():
    order_by = request.args.get('order_by')
    order = request.args.get('order')
    columns = data_manager.get_columns()
    if request.method == 'POST':
        return redirect(url_for('add_question'))
    if not order_by:
        questions = data_manager.get_questions()
    else:
        column_names = {
            'date': 'submission_time',
            'views': 'view_number',
            'votes': 'vote_number',
            'title': 'title',
            'message': 'message'
        }
        questions = data_manager.sort_questions(column_names[order_by], order)
    return render_template('questions.html', questions=questions, columns=columns.keys()


# @app.route("/question/<question_id>", methods=["GET", 'POST'])
# def display_question(question_id):
#     question = data_manager.get_question
#
#     # answers_to_be_displayed = []
#     # question_to_be_displayed = ""
#     # for row in questions:
#     #     if row['id'] == question_id:
#     #         question_to_be_displayed = row
#     #         view_num = int(row['view_number'])
#     #         view_num += 1
#     #         row['view_number'] = str(view_num)
#     #         data_manager.update_data(QUESTION_FILE_PATH, questions, connection.DATA_HEADER)
#     # for column in answers:
#     #     if column['question_id'] == question_id:
#     #         answers_to_be_displayed.append(column)
#     # for answer in answers_to_be_displayed:
#     #     answer['submission_time'] = util.convert_timestamp(float(answer.get('submission_time')))
#
#     return render_template("display_question.html", question=question_to_be_displayed, question_id=question_id, answers=answers_to_be_displayed, headers=headers)
#
#
#
# @app.route('/add_question/', methods=['GET','POST'])
# def add_question():
#     # file_name = "sample_data/question.csv"
#     if request.method == 'POST':
#         data = {
#             # 'id': util.generate_id(file_name),
#             TODO 'submission_time': util.generate_timestamp(),
#             'view_number': '0',
#             'vote_number': '0',
#             'title': request.form.get('title', ''),
#             'message': request.form.get('message', ''),
#             'image': 'images/%s' % request.files.get('image', '').filename
#         }
#         file = request.files['image']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         # connection.append_data(file_name, data)
#         id = TODO
#         return redirect(url_for('display_question', question_id=id))
#     return render_template('add_question.html')
#
#
#
@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question(question_id)
#
#     return redirect(url_for('display_questions'))
#
# @app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
# def edit_question(question_id):
#     # questions = connection.read_data(QUESTION_FILE_PATH)
#     # for question in questions:
#     #     if question['id'] == question_id:
#     #         row = question
#     if request.method == 'POST':
#         for question in questions:
#             if question['id'] == question_id:
#                 question['title'] = request.form['title']
#                 question['message'] = request.form['message']
#                 question['image'] = 'images/%s' % request.files.get('image', '').filename
#                 file = request.files['image']
#                 if file and allowed_file(file.filename):
#                     filename = secure_filename(file.filename)
#                     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 data_manager.update_data(QUESTION_FILE_PATH, questions, connection.DATA_HEADER)
#                 question_id = question['id']
#                 return redirect(url_for('display_question', question_id=question_id))
#     return render_template('edit_question.html', question=row)
#
#
# @app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
# def add_answer(question_id):
#     if request.method == "GET":
#         return render_template("add_answer.html", question_id=question_id)
#     data = {
#         # 'id': util.generate_id(ANSWER_FILE_PATH),
#         'submission_time': util.generate_timestamp(),
#         'vote_number': '0',
#         'question_id': question_id,
#         'message': request.form.get('message', ''),
#         'image': 'images/%s' % request.files.get('image', '').filename
#     }
#     file = request.files['image']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#     connection.append_data(ANSWER_FILE_PATH, data)
#     return redirect(url_for("display_question", question_id=question_id))
#
# ESZTER

@app.route("/answer/<answer_id>/vote-up", methods=['GET'])
def vote_answer_up(answer_id):
    data_manager.vote_answer_up(answer_id)
    data = data_manager.get_answer(answer_id)
    return redirect(url_for('display_question', question_id=data.question_id))


@app.route("/answer/<answer_id>/vote-down", methods=['GET'])
def vote_answer_down(answer_id):
    data_manager.vote_answer_down(answer_id)
    data = data_manager.get_answer(answer_id)
    return redirect(url_for('display_question', question_id=data.question_id))


@app.route("/question/<question_id>/vote-up", methods=['GET'])
def vote_question_up(question_id):
    data_manager.vote_question_up(question_id)
    return redirect("/list")

@app.route("/question/<question_id>/vote-down", methods=['GET'])
def vote_question_down(question_id):
    data_manager.vote_question_down(question_id))
    return redirect("/list")


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    if request.method == 'POST':
        data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=answer.question_id))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
