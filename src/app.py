import datetime
import json

from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/static')


# State is populated with dummy data for demo
# If actually using this we should store the state properly

class Game:
    def __init__(self, current_game=''):
        self.current_game = current_game
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if current_game else ''

    def __bool__(self):
        return self.current_game != ''


class Games:
    def __init__(self):
        self.current = Game('Anthony vs Jake')
        self.queue = ['Mark vs Jess', 'Patrik vs Aaron', 'Nicole vs NEK', 'Le vs The World']

    def add(self, match):
        if not match:
            return

        if self.current:
            self.queue.append(match)
        else:
            self.current = Game(match)

    def cancel(self, match):
        if match in self.queue:
            self.queue.remove(match)

    def next(self):
        if self.queue:
            self.current = Game(self.queue.pop(0))
        else:
            self.current = Game()


class Players:
    def __init__(self):
        self.looking = ['Adam']

    def add(self, name):
        if name:
            self.looking.append(name)

    def remove(self, name):
        if name in self.looking:
            self.looking.remove(name)


games = Games()
players = Players()


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html',
                           queue=games.queue,
                           current_game=games.current.current_game,
                           start_time=games.current.start_time,
                           looking_for_partners=players.looking)


@app.route('/api/match', methods=['POST'])
def add_match():
    games.add(request.form['match'])
    return redirect('/')


@app.route('/api/match/<match>', methods=['DELETE'])
def remove_match(match):
    games.cancel(match)
    return redirect('/')


@app.route('/api/quickbook', methods=['POST'])
def quick_book():
    games.add('Ad-hoc game')
    return redirect('/')


@app.route('/api/finished', methods=['POST'])
def game_over():
    games.next()
    return redirect('/')


@app.route('/api/player', methods=['POST'])
def add_player():
    players.add(request.form['name'])
    return redirect('/')


@app.route('/api/player/<name>', methods=['DELETE'])
def remove_player(name):
    players.remove(name)
    return redirect('/')


@app.route('/api/pair', methods=['POST'])
def pair_up():
    body = json.loads(request.data)
    pair_players(body['name1'], body['name2'])
    return redirect('/')


def pair_players(name1, name2):
    if name1 and name2:
        players.remove(name1)
        players.remove(name2)
        games.add(f'{name1} vs {name2}')


if __name__ == '__main__':
    app.run()
