from flask import Flask, render_template, request, redirect, url_for
import connection
import data_manager
import util
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html") #inheritence template


@app.route("/list")
def display_questions():
    if request.method == 'POST':
        return redirect(url_for('add_question'))
    questions = connection.read_data(filename="sample_data/question.csv")
    headers = connection.DATA_HEADER
    return render_template('questions.html', questions=questions, headers=headers)

    #return render_template("questions.html") #,questions=connection.read_data(questions))


#@app.route("/question/<question_id>", methods=["GET"])
@app.route("/question/<question_id>", methods=["GET"])
def display_question():
    return render_template(
        "display_question.html",
        questions=connection.read_data('sample_data/question.csv'),
        answers=connection.read_data('sample_data/answer.csv')
    )


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    filename = "sample_data/question.csv"
    if request.method == 'POST':
        data = {}
        data['id'] = util.generate_id(filename)
        data['submission_time'] = "2"
        data['view_number'] = '10'
        data['vote_number'] = '5'
        data['title'] = request.form['title']
        data['message'] = request.form['message']
        image = request.files['image']
        image.save()

        connection.append_data(filename, data)
        return redirect(url_for('display_questions'))
    return render_template('add_question.html')


# @app.route('/question/<question_id>/edit', methods=['GET', 'POST']) #Routenak kell csinalni html-t
# def add_question():
#     filename = "sample_data/question.csv"
#     if request.method == 'POST':
#         data = {}
#         data['id'] = util.generate_id(filename)
#         data['submission_time'] = "2"
#         data['view_number'] = '10'
#         data['vote_number'] = '5'
#         data['title'] = request.form['title']
#         data['message'] = request.form['message']
#         image = request.files['image']
#         image.save()

@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    filename = "sample_data/question.csv"
    if request.method == 'POST':
        data_manager.delete_question(question_id)



    return redirect(url_for('display_questions'))




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
