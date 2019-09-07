import datetime
import json

from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/static')

queue = ['Mark vs Jess', 'Patrik vs Aaron', 'Nicole vs NEK', 'Le vs The World']
looking_for_partners = ['Adam']
current_game = 'Anthony vs Jake'
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html',
                           queue=queue,
                           current_game=current_game,
                           looking_for_partners=looking_for_partners,
                           start_time=start_time)


@app.route('/api/add', methods=['POST'])
def add_to_queue():
    match = request.form['match']
    add_match(match)
    return redirect('/')


def add_match(match):
    if not match:
        return

    global current_game
    global start_time
    if current_game:
        queue.append(match)
    else:
        current_game = match
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


@app.route('/api/delete/<match>', methods=['POST'])
def remove_from_queue(match):
    if match in queue:
        queue.remove(match)
    return redirect('/')


@app.route('/api/finished', methods=['POST'])
def game_over():
    global current_game
    global start_time
    if queue:
        current_game = queue.pop(0)
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        current_game = ''
        start_time = ''
    return redirect('/')


@app.route('/api/quickbook', methods=['POST'])
def quick_book():
    add_match('Ad-hoc game')
    return redirect('/')


@app.route('/api/needpartner', methods=['POST'])
def add_to_looking_queue():
    name = request.form['name']
    if name:
        looking_for_partners.append(name)
    return redirect('/')


@app.route('/api/deletelooking/<name>', methods=['POST'])
def remove_from_looking_queue(name):
    if name in looking_for_partners:
        looking_for_partners.remove(name)
    return redirect('/')


@app.route('/api/pairme', methods=['POST'])
def pair_up():
    body = json.loads(request.data)
    name1 = body['name1']
    name2 = body['name2']
    if name1 and name2:
        if name1 in looking_for_partners:
            looking_for_partners.remove(name1)
        if name2 in looking_for_partners:
            looking_for_partners.remove(name2)
        add_match(f'{name1} vs {name2}')
    return redirect('/')


if __name__ == '__main__':
    app.run()
