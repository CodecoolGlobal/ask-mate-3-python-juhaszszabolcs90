from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

import connection
import util

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
def hello():
    return render_template("index.html") #inheritence template


@app.route("/list")
def display_questions():
    if request.method == 'POST':
        return redirect(url_for('add_question'))
    questions = connection.read_questions(filename="sample_data/question.csv")
    headers = connection.DATA_HEADER
    return render_template('questions.html', questions=questions, headers=headers)

    #return render_template("questions.html") #,questions=connection.read_data(questions))


@app.route("/question/<question_id>", methods=["GET"])
def display_question():
    return render_template(
        "question.html",
        questions=connection.read_data(questions),
        answers=connection.read_data(answers)
    )


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    file_name = "sample_data/question.csv"
    if request.method == 'POST':
        data = {
            'id': util.generate_id(file_name),
            'submission_time': "2",
            'view_number': '10',
            'vote_number': '5',
            'title': request.form.get('title', ''),
            'message': request.form.get('message', ''),
            'image': 'images/%s' % request.files.get('image', '').filename
        }
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        connection.write_question(file_name, data)
        return redirect(url_for('display_questions'))
    return render_template('add_question.html')


"""""
@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    data_manager.write_to_file(questions, request.form)
    return redirect(url_for("display_question")) #---> a saját, most generált ID-ja kell a kérdésnek
"""


"""
@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer():
    if request.method == "GET"
        return render_template("add_answer.html")
    data_manager.write_to_file(answers, request.form)
    return redirect(url_for("display_question"))
"""


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
