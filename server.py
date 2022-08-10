from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from psycopg2.errors import UniqueViolation
from datetime import timedelta
import data_manager

from bonus_questions import SAMPLE_QUESTIONS

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/images'


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'\x1dH@\xb94\xc9\xb0\x8e\xd5\xa8\xfe\\r\x00\x0c\xb4'
app.permanent_session_lifetime = timedelta(minutes=10)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/")
def index():
    data_manager.delete_empty_questions()
    questions = data_manager.get_five_latest_questions()
    if 'username' in session:
        username = session['username']
        flash(f'You are logged in as {username}')
        return render_template('index.html', questions=questions, username=username)

    return render_template('index.html', questions=questions)


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
    for_order_by = request.args.get('sort', 'title|ASC').split('|')
    order_by = for_order_by[0]
    order = for_order_by[1]

    questions = data_manager.get_and_sort_questions(column_names[order_by], order)
    return render_template('questions.html', questions=questions, columns=column_names.keys(), order=['ASC', 'DESC'], sort=request.args.get('sort'))


@app.route("/question/<question_id>", methods=["GET", 'POST'])
def display_question(question_id):
    data_manager.update_question_view_number(question_id)
    question = data_manager.get_question(question_id)
    answers = data_manager.get_answers_to_question(question.get('id'))
    answers_comment = data_manager.get_answers_comment_by_question_id(question.get('id'))
    comment_messages = data_manager.get_comments_about_question(question_id)
    tags = data_manager.get_tags(question_id)
    return render_template("display_question.html", question=question, answers=answers, tags=tags, comments=comment_messages, answers_comment=answers_comment, question_id=question_id)


@app.route('/add_question/', methods=['GET', 'POST'])
def add_question():
    username = session.get('username', 'lazlo') # replace with if username in session
    logged_in_user = data_manager.get_user(username)
    user_id = logged_in_user['id']
    title = ''
    message = ''
    image = None
    if data_manager.get_question_by_title(title) is None:
        new_question = data_manager.add_question(user_id, title, message, image)
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


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment_question(comment_id):
    comment = data_manager.get_comment(comment_id)
    answer = data_manager.get_answer(comment.get('answer_id'))
    if request.method == 'POST':
        data_manager.update_edit_count_to_comment(comment_id)
        message = request.form.get('message')
        data_manager.update_comment_question(comment_id, message)
        return redirect(url_for("display_question", question_id=answer.get('question_id')))
    return render_template("edit_question_comment.html", comment=comment)


@app.route('/search')
def search():
    search_results = data_manager.search(request.args.get('search'))
    return render_template('search_results.html', search_results=search_results)


@app.route('/add_tags/<question_id>', methods=['POST'])
def add_tags(question_id):
    if request.method == 'POST':
        try:
            tag_id = data_manager.add_tag(request.form.get('tag'))
            data_manager.add_question_tag(question_id, tag_id.get('id'))
        except UniqueViolation:
            tag_id = data_manager.get_tag(request.form.get('tag'))
            data_manager.add_question_tag(question_id, tag_id.get('id'))
        tags = data_manager.get_tags(question_id)
        return redirect(url_for('add_question', tags=tags))


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


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    username = session.get('username', 'lazlo') # replace with if username in session
    logged_in_user = data_manager.get_user(username)
    user_id = logged_in_user['id']
    if request.method == 'POST':
        message = request.form.get('message')
        data_manager.add_answer(user_id, message, question_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_answer.html', question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_comment_to_answer(answer_id):
    username = session.get('username', 'lazlo') # replace with if username in session
    logged_in_user = data_manager.get_user(username)
    user_id = logged_in_user['id']
    if request.method == 'POST':
        answer_comment_message = request.form.get('comment')
        data_manager.add_comment_to_answer(user_id, answer_id, answer_comment_message)
        data = data_manager.get_answer(answer_id)
        return redirect(url_for('display_question', question_id=data.get('question_id')))
    return render_template('add_comment_to_answer.html', answer_id=answer_id)


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


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_comment(question_id):
    if request.method == 'POST':
        comment_message = request.form.get('message')
        data_manager.add_comment(question_id, comment_message)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add_comment.html', question_id=question_id)


@app.route("/comments/<comment_id>/delete", methods=["GET", "POST"])
def delete_comment(comment_id):
    if request.method == 'POST':
        data_manager.delete_comment(comment_id)
        question_id = request.form.get('questionID')
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/delete_tag/<id>', methods=['GET', 'POST'])
def delete_tag(id):
    question_tag_id = data_manager.get_question_id_for_tag(id)
    data_manager.delete_tag(id)
    return redirect(url_for('display_question', question_id=question_tag_id.get('question_id')))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        plain_text_password = request.form['psw']
        hashed_password = data_manager.hash_password(plain_text_password)
        # data_manager.users[username] = hashed_password
        data_manager.add_users(username,email,hashed_password)
        # session['username'] = username
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        plain_text_password = request.form['psw']
        user_data = data_manager.get_user(username)
        if user_data is not None:
            password = user_data['password']
            if data_manager.verify_password(plain_text_password, password):
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


@app.route('/users')
def users():
    if 'username' in session:
        users_data = data_manager.list_users()
        return render_template('users.html', users_data=users_data)
    else:
        flash(f'you need to be logged in to check users')
        return redirect(url_for('index'))

@app.route('/user/<user_name>')
def user(user_name):
    if 'username' in session:
        user_data = data_manager.get_user(user_name)
        user_answer_question_comment_count = data_manager.get_user_answer_question_comment_count(user_name)
        user_answer_list = data_manager.get_user_answer_list(user_name)
        user_question_list = data_manager.get_user_question_list(user_name)
        user_comment_list = data_manager.get_user_comment_list(user_name)
        return render_template('user_page.html', user_data=user_data,user_answer_question_comment=user_answer_question_comment_count,answer_list=user_answer_list, question_list=user_question_list,comment_list=user_comment_list)
    else:
        flash(f'you need to be logged in to check users')
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )
