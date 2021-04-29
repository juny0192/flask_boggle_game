from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def setUp(self):
        """Made repetitive code line as an starter on every test"""

        self.client = app.test_client()
        
    def test_boggle_main(self):
        """Simple main page checking"""
        
        res = self.client.get('/')
        html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1>BOGGLE GAME</h1>', html)

    def test_game_board(self):
        """Checking if stuffs are displayed well on html"""

        with self.client:
            res = self.client.get('/board')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('<p>High score: 0</p>', html)
            self.assertIn('<p>Total play times: 0</p>',html)

    def test_valid_word(self):
        """Checking if finding valid word function is working well"""

        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["D", "O", "G", "D", "O"], 
                                           ["D", "O", "G", "D", "O"], 
                                           ["D", "O", "G", "D", "O"], 
                                           ["D", "O", "G", "D", "O"], 
                                           ["D", "O", "G", "D", "O"]]
            res = self.client.get('/check?q=dog')

            self.assertEqual(res.json["result"], "ok")

    def test_invalid_word(self):
        """Checking if invalid_word function is working well"""

        self.client.get('/board')
        res = self.client.get('/check?q=hello')

        self.assertEqual(res.json["result"], "not-on-board")

    def test_non_eng_word(self):
        """Checking if the word is Eng or not"""

        self.client.get('/board')
        res = self.client.get('/check?q=lololol')

        self.assertEqual(res.json["result"], "not-word")
    

