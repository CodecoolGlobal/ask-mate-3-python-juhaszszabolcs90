from flask import Flask, render_template, request, redirect, url_for
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html") #inheritence template


@app.route("/list")
def display_questions():
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


@app.route('/add_question/<id>', methods=['GET','POST'])
def story():
    if request.method == 'POST':
        user_story = {}
        user_story['id'] = data_handler.generate_id()
        user_story['title'] = request.form['title']
        user_story['user_story'] = request.form['story']
        user_story['acceptance_criteria'] = request.form['acceptance-criteria']
        user_story['business_value'] = request.form['value']
        user_story['estimation'] = request.form['estimation']
        user_story['status'] = 'planning'

        data_handler.add_user_story(user_story)
        return redirect('/')
    return render_template('story.html')

@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    return render_template("add_question.html")

"""
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
