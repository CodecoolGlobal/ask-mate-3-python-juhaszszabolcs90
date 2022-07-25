# DATA MANAGER

def delete_question(id_question):
    filtered_questions = filter(lambda question: question['id'] != id_question, questions)
    connection.write_data('sample_data/question.csv', list(filtered_questions))


def search_id_by_question(id):
    data = connection.read_data('sample_data/question.csv')
    for row in data:
        if row['id'] == id:
            return row

def sort_data(data, sort_by='submission_time', reverse=False):
    return sorted(data, key=operator.itemgetter(sort_by), reverse=reverse)

# SERVER

@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer(question_id):
    if request.method == "POST":
        data = {
            'id': util.generate_id("sample_data/answer.csv"),
            'submission_time': util.generate_timestamp(),
            'vote_number': '0',
            'question_id': question_id,
            'message': request.form['message'],
        }
        connection.append_data("sample_data/answer.csv", data)
        return redirect(url_for('display_question', question_id = question_id))

    return render_template("add_answer.html", question_id=question_id)

# TEMPLATES

# ADD ANSWER
<!DOCTYPE html>
<html lang="en">
<head>
        <meta charset="UTF-8">
        <title>Add Answer</title>
    </head>
<body>
    <h1>Add an answer for this question</h1>
    <form action="/question/{{ question_id }}/new-answer" method="POST" enctype="multipart/form-data">
        <label for="message">Message:</label><br>
        <textarea id="message" name="message" rows="8" cols="50" required></textarea><br>

        <input type="file" id="picture" name="picture" accept="image/" >
        <button type="submit" name="submitBtn">Submit Answer</button>
    </form>
</body>
</html>

# DISPLAY QUESTION
                   {% if data['image'] == 'images/' or data['image'] == None or data['image'] == '' %}
                        <td></td>
                    {% else %}
                    <td><img src="{{ url_for('static', filename=data['image']) }}" alt='{{ data['image'] }}' width="100" >
                    </td>
                    {% endif %}
                    <form><form action={{ url_for( 'delete_answer', answer_id = data['id']) }} method = 'POST'>
                        <button type='submit' class="delete-btn">Delete
                    </button></form>
                        </button>
                    </form>
                        </td>

                    </td>
                </tr>
            {% endfor %}
            </table><br><br>
        <button> <a href="{{ url_for('display_questions') }}">Back to list of questions</a> </button>
        <table>
        <form action={{ url_for('add_answer',question_id = question['id']) }} method = 'GET'>
        <button type='submit' class >Add new answer </button>
        </form>
    </table>
    </body>
</html>