from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from psycopg2.errors import UniqueViolation
from datetime import timedelta
import data_manager, hashing, server_functions

from bonus_questions import SAMPLE_QUESTIONS

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/images'


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'\x1dH@\xb94\xc9\xb0\x8e\xd5\xa8\xfe\\r\x00\x0c\xb4'
app.permanent_session_lifetime = timedelta(minutes=30)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/bonus-questions")
def main():
    if 'username' in session:
        username = session['username']
        flash(f'You are logged in as {username}', category='info')
        return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)
    flash(f'You need to be logged in to check Bonus questions', category='info')
    return redirect(url_for('index'))

# INDEX


@app.route("/")
def index():
    data_manager.delete_empty_questions()
    questions = data_manager.get_five_latest_questions()
    if 'username' in session:
        username = session['username']
        flash(f'You are logged in as {username}', category='info')
        return render_template('index.html', questions=questions, username=username)

    return render_template('index.html', questions=questions)


# QUESTIONS


@app.route("/list", methods=['GET', 'POST'])
def display_questions():
    data_manager.delete_empty_questions()
    column_names = {
        'date': 'submission_time',
        'views': 'view_number',
        'votes': 'vote_number',
        'title': 'title',
        'message': 'message'
    }
    questions = server_functions.get_ordered_questions(column_names)
    return render_template('questions.html', questions=questions, columns=column_names.keys(), order=['ASC', 'DESC'], sort=request.args.get('sort'))


@app.route('/add_question/', methods=['GET', 'POST'])
def add_question():
    title = ''
    message = ''
    image = None
    user = data_manager.get_user(session.get('username'))
    if data_manager.get_question_by_title(title) is None:
        new_question = data_manager.add_question(user.get('id'), title, message, image)
    else:
        new_question = data_manager.get_question_by_title(title)
    tags = data_manager.get_tags(new_question.get('id'))
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        if request.files.get('image').filename != '':
            image = 'images/%s' % request.files.get('image', '').filename
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data_manager.update_question_with_time(new_question.get('id'), title, message, image)
        return redirect(url_for('display_question', question_id=new_question.get('id')))
    return render_template('add_question.html', question_id=new_question.get('id'), tags=tags)


@app.route("/question/<question_id>", methods=["GET", 'POST'])
def display_question(question_id):
    data_manager.update_question_view_number(question_id)
    question_information = server_functions.get_question_information(question_id)
    return render_template(
        "display_question.html",
        question=question_information['question'],
        answers=question_information['answers'],
        tags=question_information['tags'],
        comments=question_information['comment_messages'],
        answers_comment=question_information['answers_comment'],
        user=question_information['user'],
        question_id=question_id
    )


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
        image = None
        if request.files.get('image').filename != '':
            image = 'images/%s' % request.files.get('image', '').filename
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data_manager.update_question(question_id, title, message, image)
        return redirect(url_for("display_question", question_id=question_id))
    else:
        question = data_manager.get_question(question_id)
        return render_template("edit_question.html", question=question)


@app.route("/question/<question_id>/vote-up", methods=['GET'])
def vote_question_up(question_id):
    user_id = data_manager.get_user_id_by_question_id(question_id)
    data_manager.vote_question_up(question_id, user_id.get('user_id'))
    return redirect("/list")


@app.route("/question/<question_id>/vote-down", methods=['GET'])
def vote_question_down(question_id):
    user_id = data_manager.get_user_id_by_question_id(question_id)
    data_manager.vote_question_down(question_id, user_id.get('user_id'))
    return redirect("/list")

# TAGS


@app.route('/add_tags/<question_id>', methods=['POST'])
def add_tags(question_id):
    if request.method == 'POST':
        try:
            try:
                tag_id = data_manager.add_tag(request.form.get('tag'))
                data_manager.add_question_tag(question_id, tag_id.get('id'))
            except UniqueViolation:
                tag_id = data_manager.get_tag(request.form.get('tag'))
                data_manager.add_question_tag(question_id, tag_id.get('id'))
        except UniqueViolation:
            pass
        tags = data_manager.get_tags(question_id)
        return redirect(url_for('add_question', tags=tags))


@app.route('/delete_tag/<id>', methods=['GET', 'POST'])
def delete_tag(id):
    question_tag_id = data_manager.get_question_id_for_tag(id)
    data_manager.delete_tag(id)
    return redirect(url_for('display_question', question_id=question_tag_id.get('question_id')))


@app.route('/tags', methods=['GET', 'POST'])
def list_tags():
    listed_tags = data_manager.list_tags()
    return render_template('tag_page.html', listed_tags=listed_tags)


# ANSWERS


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    user = data_manager.get_user(session.get('username', None))
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_answer(user.get('id'), message, question_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html', question_id=question_id)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.edit_answer(answer_id, message)
        answer = data_manager.get_answer(answer_id)
        return redirect(url_for("display_question", question_id=answer.get('question_id')))
    else:
        answer = data_manager.get_answer(answer_id)
        return render_template("edit_answer.html", answer=answer)


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    if request.method == 'POST':
        data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question', question_id=answer.get('question_id')))


@app.route("/answer/<answer_id>/vote-up", methods=['GET'])
def vote_answer_up(answer_id):
    data = data_manager.get_answer(answer_id)
    user_id = data_manager.get_user_id_by_answer_id(answer_id)
    data_manager.vote_answer_up(answer_id, user_id.get('user_id'))
    return redirect(url_for('display_question', question_id=data.get('question_id')))


@app.route("/answer/<answer_id>/vote-down", methods=['GET'])
def vote_answer_down(answer_id):
    data = data_manager.get_answer(answer_id)
    user_id = data_manager.get_user_id_by_answer_id(answer_id)
    data_manager.vote_answer_down(answer_id, user_id.get('user_id'))
    return redirect(url_for('display_question', question_id=data.get('question_id')))


@app.route("/answer/<answer_id>/accept", methods=['GET'])
def accept_answer(answer_id):
    answer = data_manager.get_answer(answer_id)
    print(answer)
    acceptions = [accept_state for accept_state in data_manager.get_answers_to_question(answer.get('question_id')) if accept_state.get('accepted')]
    question = data_manager.get_question(answer.get('question_id'))
    question_user = data_manager.get_user_by_id(question.get('user_id'))
    if session.get('username') == question_user.get('user_name'):
        if answer.get('accepted') is False and len(acceptions) == 0:
            data_manager.accept_answer(answer_id, 'True')
            data_manager.increase_honor_by_accepted_answer(answer.get('user_id'))
        elif answer.get('accepted') is True:
            data_manager.accept_answer(answer_id, 'False')
            data_manager.decrease_honor_by_accepted_answer(answer.get('user_id'))
    return redirect(url_for('display_question', question_id=answer.get('question_id')))


# COMMENTS


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_comment(question_id):
    if 'username' in session:
        user = data_manager.get_user(session.get('username'))
        if request.method == 'POST':
            comment_message = request.form.get('message')
            data_manager.add_comment(question_id, comment_message, user.get('id'))
            return redirect(url_for('display_question', question_id=question_id))
        return render_template('add_comment.html', question_id=question_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment_question(comment_id):
    comment = data_manager.get_comment(comment_id)
    question = data_manager.get_question(comment.get('question_id'))
    if request.method == 'POST':
        data_manager.update_edit_count_to_comment(comment_id)
        message = request.form.get('message')
        data_manager.update_comment_question(comment_id, message)
        return redirect(url_for("display_question", question_id=question.get('id')))
    return render_template("edit_question_comment.html", comment=comment)


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    user = data_manager.get_user(session.get('username'))
    if request.method == 'POST':
        answer_comment_message = request.form.get('comment')
        data_manager.add_comment_to_answer(user.get('id'), answer_id, answer_comment_message)
        data = data_manager.get_answer(answer_id)
        return redirect(url_for('display_question', question_id=data.get('question_id')))
    return render_template('add_comment_to_answer.html', answer_id=answer_id)


@app.route("/comments/<comment_id>/delete", methods=["GET", "POST"])
def delete_comment(comment_id):
    if request.method == 'POST':
        data_manager.delete_comment(comment_id)
        question_id = request.form.get('questionID')
    return redirect(url_for('display_question', question_id=question_id))


# SEARCH


@app.route('/search')
def search():
    search_results = data_manager.search(request.args.get('search'))
    return render_template('search_results.html', search_results=search_results)


# USERS, REGISTER, LOGIN/LOGOUT


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        hashed_password = hashing.hash_password(request.form['psw'])
        # data_manager.users[username] = hashed_password
        data_manager.add_users(username,email,hashed_password)
        # session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/users')
def users():
    if 'username' in session:
        users_data = data_manager.list_users()
        print(users_data)
        return render_template('users.html', users_data=users_data)
    flash(f'you need to be logged in to check users')
    return redirect(url_for('index'))


@app.route('/user/<user_name>')
def user(user_name):
    if 'username' in session:
        user_name = user_name
        user_data = data_manager.get_user(user_name)
        user_answer_question_comment_count = data_manager.get_user_answer_question_comment_count(user_name)
        user_answer_list = data_manager.get_user_answer_list(user_name)
        user_question_list = data_manager.get_user_question_list(user_name)
        user_comment_list = data_manager.get_user_comment_list(user_name)
        print(user_comment_list)
        # user_comment_list['']
        return render_template('user_page.html', user_data=user_data,
                               user_answer_question_comment=user_answer_question_comment_count,
                               answer_list=user_answer_list, question_list=user_question_list,
                               comment_list=user_comment_list)
    else:
        flash(f'you need to be logged in to check users')
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_data = data_manager.get_user(username)
        if user_data is not None:
            password = user_data['password']
            if hashing.verify_password(request.form['psw'], password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                flash(f'Password is incorrect')
                return redirect(url_for('login'))
        else:
            flash(f'No such as username as: {username} and password combination')
            return redirect(url_for('login'))
    else:
        if "user" in session:
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        username = session['username']
        session.clear()
    # session.pop("user", None)
    flash(f'You have been logged out {username}')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
































