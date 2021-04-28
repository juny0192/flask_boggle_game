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
    """main homepage"""

    return render_template('main.html')

@app.route('/board')
def game_start():
    """board-game page"""

    board = boggle_game.make_board()
    session["board"] = board
    highScore = session.get("highScore", 0)
    nTimesPlay = session.get("nTimesPlay", 0)

    return render_template('board.html', board = board, highScore= highScore, nTimesPlay = nTimesPlay)

@app.route('/check')
def check_word():
    """check if the submitted word is a valid English"""

    searchVal = request.args["q"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, searchVal)
    return jsonify({'result': result})

@app.route('/post-score', methods=["POST"])
def post_score():
    score = request.json["score"]
    highScore = session.get("highScore", 0)
    nTimesPlay = session.get("nTimesPlay", 0)

    session["nTimesPlay"] = nTimesPlay + 1
    session["highScore"] = max(score, highScore)

    return jsonify({'newRecord': score > highScore})
