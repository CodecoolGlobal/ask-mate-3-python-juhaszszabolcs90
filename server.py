from flask import Flask, render_template, request, redirect, url_for
import connection
import util

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html") #inheritence template


@app.route("/list")
def display_questions():
    questions = connection.read_data(filename="sample_data/question.csv")
    headers = connection.DATA_HEADER
    return render_template('questions.html', questions=questions, headers=headers)

    #return render_template("questions.html") #,questions=connection.read_data(questions))


@app.route("/question/<question_id>", methods=["GET"])
def display_question(id):
    return render_template(
        "display_question.html",
        questions=connection.read_data("sample_data/question.csv"),
        answers=connection.read_data("sample_data/answer.csv")
    )


@app.route('/add_question/', methods=['GET','POST'])
def add_question():
    if request.method == 'POST':
        filename = "sample_data/question.csv"
        data = {}
        data['id'] = util.generate_id(filename)
        data['submission_time'] = "2"
        data['view_number'] = '10'
        data['vote_number'] = '5'
        data['title'] = request.form['title']
        data['message'] = request.form['message']
        data['image'] = request.form['image']

        connection.write_data(filename, data)
        id = data.get('id')
        return redirect(url_for(f'display_question({id})'))
    return render_template('add_question.html')



"""
@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer():
    if request.method == "GET"
        return render_template("add_answer.html")
    data_manager.write_to_file(answers, request.form)
    return redirect(url_for("display_question"))
"""

@app.route("/answer/<answer_id>/vote-up", methods=['GET'])
def vote_up_answer(id):
    user_stories = data_handler.get_all_user_story()

    for row in user_stories:
        if row['id'] == str(user_story['id']):
            user_stories[user_stories.index(row)] = user_story

    data_handler.update_user_story(user_stories)
    return redirect('/')

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
