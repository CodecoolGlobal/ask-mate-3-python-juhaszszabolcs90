from flask import Flask, render_template, request, redirect, url_for
import connnection

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html") #inheritence template


@app.route("/list", methods=["GET"])
def display_questions():
    return render_template(
        "questions.html",
        questions=connection.read_data(questions)
    )


@app.route("/question/<question_id>", methods=["GET"])
def display_question():
    return render_template(
        "question.html",
        questions=connection.read_data(questions),
        answers=connection.read_data(answers)
    )


@app.route("/add-question", methods=["GET", "POST"]
def add_question():
    if request.method == "GET":
        return render_template(
            "add_question.html",
        )

    return redirect(url_for("display_question"))


if __name__ == "__main__":
    app.run(
        debug=True
        port=5000,
    )
