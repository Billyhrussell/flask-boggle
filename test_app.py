from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- This is the index.html page for testing -->', html)
            # test that you're getting a template

    def test_api_new_game(self):
        """Test starting a new game.
        1. check if return JSON
        2. check if JSON has a string called "gameId"
        and a nested list [[5 letters]x5](=board)
        3. check that games dict contains new game"""

        with self.client as client:
            resp = client.post("/api/new-game")
            JSON = resp.get_json()

            self.assertEqual(resp.is_json, True)
            self.assertTrue(type(JSON["gameId"]) == str)

            self.assertTrue(type(JSON['board']))
            self.assertTrue(len(JSON['board']) == 5)

            self.assertTrue(type(JSON['board'][0]))
            self.assertTrue(len(JSON['board'][0]) == 5)

            self.assertTrue(games.__contains__(JSON['gameId']))

    def test_for_word(self):
        with self.client as client:
            resp = client.post("/api/new-game")
            JSON = resp.get_json()

            game_id = JSON["gameId"]
            game = games[game_id]
            game.board = [["C","A","T","X", "X"],
             ["C","A","T","X", "X"], ["C","A","T","X", "X"],
             ["C","A","T","X", "X"], ["C","A","T","X", "X"]]
            resp = client.post("/api/score-word", json = {"game_id" : game_id, "word" : "CAT"})

            json = resp.get_json()
            self.assertEqual(json, {"result" : "ok"})

            game_id = JSON["gameId"]
            game = games[game_id]
            game.board = [["C","A","T","X", "X"],
             ["C","A","T","X", "X"], ["C","A","T","X", "X"],
             ["C","A","T","X", "X"], ["C","A","T","X", "X"]]
            resp = client.post("/api/score-word", json = {"game_id" : game_id, "word" : "$$$"})

            json = resp.get_json()
            self.assertEqual(json, {"result" : "not-word"})

            game_id = JSON["gameId"]
            game = games[game_id]
            game.board = [["C","A","T","X", "X"],
             ["C","A","T","X", "X"], ["C","A","T","X", "X"],
             ["C","A","T","X", "X"], ["C","A","T","X", "X"]]
            resp = client.post("/api/score-word", json = {"game_id" : game_id, "word" : "WOW"})

            json = resp.get_json()
            self.assertEqual(json, {"result" : "not-on-board"})





