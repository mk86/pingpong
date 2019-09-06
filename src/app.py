from flask import Flask, render_template, request, redirect

app = Flask(__name__)

queue = []
current_game = ''


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html', queue=queue, current_game=current_game)


@app.route('/api/add', methods=['POST'])
def add_to_queue():
    match = request.form['match']
    if match:
        global current_game
        if current_game:
            queue.append(match)
        else:
            current_game = match
    return redirect('/')


@app.route('/api/finished', methods=['POST'])
def game_over():
    global current_game
    if queue:
        current_game = queue.pop(0)
    else:
        current_game = ''
    return redirect('/')


if __name__ == '__main__':
    app.run()
