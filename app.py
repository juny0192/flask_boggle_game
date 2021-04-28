from boggle import Boggle
from flask import Flask, request, render_template, redirect, session
from flask import jsonify
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "juny0192"
app.debug = True

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/board')
def game_start():
    board = boggle_game.make_board()
    session["board"] = board
    return render_template('board.html', board = board)

@app.route('/check')
def check_word():
    searchVal = request.args["q"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, searchVal)
    return jsonify({'result': result})


    
    