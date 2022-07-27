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
def index():
    questions = data_manager.get_five_latest_questions()
    return render_template('index.html', questions=questions)



@app.route("/list")
def display_questions():
    if request.args.get('sort'):
        for_order_by = request.args.get('sort').split('|')
        order_by = for_order_by[0]
        order = for_order_by[1]
    columns = data_manager.get_columns()
    if request.method == 'POST':
        return redirect(url_for('add_question'))
    if not request.args.get('sort'):
        questions = data_manager.get_and_sort_questions()
    else:
        column_names = {
            'date': 'submission_time',
            'views': 'view_number',
            'votes': 'vote_number',
            'title': 'title',
            'message': 'message'
        }
        questions = data_manager.get_and_sort_questions(column_names[order_by], order)
    return render_template('questions.html', questions=questions, columns=columns.keys(), order=['ASC', 'DESC'], sort=request.args.get('sort'))


@app.route("/question/<question_id>", methods=["GET", 'POST'])
def display_question(question_id):
    data_manager.update_question_view_number(question_id)
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers_to_question(question.get('id'))
    return render_template("display_question.html", question=question, answers=answers)


@app.route('/add_question/', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = None
        if request.files.get('image').filename != '':
            image = 'images/%s' % request.files.get('image', '').filename
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        added_question = data_manager.add_question(title, message, image)
        return redirect(url_for('display_question', question_id=added_question.get('id')))
    return render_template('add_question.html')


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question(question_id)
    return redirect(url_for('display_questions'))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        image = 'images/%s' % request.files.get('image', '').filename
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data_manager.update_question(question_id, title, message, image)
        return redirect(url_for("display_questions"))
    else:
        question = data_manager.get_question(question_id)
        return render_template("edit_question.html", question=question)


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_answer(message, question_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html', question_id=question_id)


@app.route("/answer/<answer_id>/vote-up", methods=['GET'])
def vote_answer_up(answer_id):
    data_manager.vote_answer_up(answer_id)
    data = data_manager.get_answer(answer_id)
    return redirect(url_for('display_question', question_id=data.get('question_id')))


@app.route("/answer/<answer_id>/vote-down", methods=['GET'])
def vote_answer_down(answer_id):
    data_manager.vote_answer_down(answer_id)
    data = data_manager.get_answer(answer_id)
    return redirect(url_for('display_question', question_id=data.get('question_id')))


@app.route("/question/<question_id>/vote-up", methods=['GET'])
def vote_question_up(question_id):
    data_manager.vote_question_up(question_id)
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=['GET'])
def vote_question_down(question_id):
    data_manager.vote_question_down(question_id)
    return redirect("/list")


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    if request.method == 'POST':
        data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=answer.get('question_id')))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
