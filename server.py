from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import connection
import data_manager
import util

import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/images'

QUESTION_FILE_PATH = "sample_data/question.csv"
ANSWER_FILE_PATH = "sample_data/answer.csv"

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/list")
def display_questions():
    if request.method == 'POST':
        return redirect(url_for('add_question'))
    questions = connection.read_data(filename=QUESTION_FILE_PATH)
    headers = util.convert_headers()
    return render_template('questions.html', questions=questions, headers=headers)


@app.route("/question/<question_id>", methods=["GET"])
def display_question(question_id):
    questions = connection.read_data(QUESTION_FILE_PATH)
    for row in questions:
        if row['id'] == question_id:
            question_to_be_displayed = row

    return render_template("display_question.html", question=question_to_be_displayed, question_id=question_id)



@app.route('/add_question/', methods=['GET','POST'])
def add_question():
    file_name = "sample_data/question.csv"
    if request.method == 'POST':
        data = {
            'id': util.generate_id(file_name),
            'submission_time': util.generate_timestamp()
            'view_number': '10',
            'vote_number': '0',
            'title': request.form.get('title', ''),
            'message': request.form.get('message', ''),
            'image': 'images/%s' % request.files.get('image', '').filename
        }
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        connection.append_data(file_name, data)
        id = data.get('id')
        return redirect(url_for('display_question', id=id))
    return render_template('add_question.html')



@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    if request.method == 'POST':
        data_manager.delete_question(question_id)

    return redirect(url_for('display_questions'))


"""
@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer():
    if request.method == "GET"
        return render_template("add_answer.html")
    data_manager.write_to_file(answers, request.form)
    return redirect(url_for("display_question"))
"""


@app.route("/answer/<answer_id>/vote-up", methods=['GET'])
def vote_answer_up(id):
    util.vote(ANSWER_FILE_PATH)
    return redirect(url_for(f'display_question({id})'))

@app.route("/answer/<answer_id>/vote-down", methods=['GET'])
def vote_answer_down(id):
    util.vote(ANSWER_FILE_PATH, False)
    return redirect(url_for(f'display_question({id})'))


@app.route("/question/<question_id>/vote-up", methods=['GET'])
def vote_question_up(id):
    util.vote(QUESTION_FILE_PATH)
    return redirect("/list")

@app.route("/question/<question_id>/vote-down", methods=['GET'])
def vote_question_down(id):
    util.vote(QUESTION_FILE_PATH, False)
    return redirect("/list")


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
