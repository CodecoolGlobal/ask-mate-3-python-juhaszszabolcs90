from flask import Flask, render_template, request, redirect, url_for
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html") #inheritence template


@app.route("/list")
def display_questions():
    questions = connection.read_questions()
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



@app.route("/add-question", methods=["GET", "POST"])
def add_question():
    if request.method == "GET":
        return render_template("add_question.html")
    data_manager.write_to_file(questions, [request.form.get("title"), request.form.get("message")])
    #kell egy fv. data_handlerbe, ami legenerálja a diktet és beírja csv-be, érdemes egy lista paraméter, hogy
    #potenciálisan több form fieldet is kezelni tudjon (pl ha tesz bele képet)
    return redirect(url_for("display_question")) #---> a saját, most generált ID-ja kell a kérdésnek


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer():
    if request.method == "GET".
        return render_template("add_answer.html")
    data_manager.write_to_file(answers, [request.form.get("message")])
    return redirect(url_for("display_question"))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
