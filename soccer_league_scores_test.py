import unittest
from soccer_league_scores import SoccerLeagueScores


class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.line_input_tie = "Lions 1, FC Awesome 1"
        self.first_result = {'name': 'Lions', 'score': 1}
        self.second_result = {'name': 'FC Awesome', 'score': 1}
        self.dict_scores_tie = {'first': self.first_result, 'second': self.second_result}

        self.line_input_win_lose = "Tarantulas 3, Snakes 1"
        self.win_result = {'name': 'Tarantulas', 'score': 3, 'points': 3}
        self.lose_result = {'name': 'Snakes', 'score': 1, 'points': 0}
        self.dict_scores_win_lose = {'first': self.win_result, 'second': self.lose_result}

        self.first_tie_result = {'name': 'Lions', 'score': 1, 'points': 1}
        self.second_tie_result = {'name': 'FC Awesome', 'score': 1, 'points': 1}

        self.ranking_first = "1. Tarantulas, 3 pts"
        self.ranking_second = "2. Snakes, 0 pts"

    def test_extract_line_input(self):
        soccer = SoccerLeagueScores()
        score = soccer.extract_line_input(self.line_input_tie)
        self.assertEqual(score['first'], self.first_result)
        self.assertEqual(score['second'], self.second_result)

    def test_adding_scores_win_lose(self):
        soccer = SoccerLeagueScores()
        soccer.add_game_score(self.dict_scores_win_lose)
        self.assertEqual(soccer.scores.get('Tarantulas'), self.win_result)  # won score to add
        self.assertEqual(soccer.scores.get('Snakes'), self.lose_result)  # lose score to add

    def test_adding_scores_tie(self):
        soccer = SoccerLeagueScores()
        soccer.add_game_score(self.dict_scores_tie)
        self.assertEqual(soccer.scores.get('Lions'), self.first_tie_result)  # tie score to add
        self.assertEqual(soccer.scores.get('FC Awesome'), self.second_tie_result)  # tie score to add

    def test_ranking(self):
        soccer = SoccerLeagueScores()
        soccer.add_game_score(self.dict_scores_win_lose)
        rankings = soccer.rank_scores()
        self.assertEqual(rankings[0], self.ranking_first)  # score 3 first
        self.assertEqual(rankings[1], self.ranking_second)  # score 1 second

    def test_tie_ranking(self):
        soccer = SoccerLeagueScores()
        soccer.add_game_score(self.dict_scores_tie)
        soccer.add_game_score(self.dict_scores_win_lose)
        ranking = soccer.rank_scores()
        self.assertEqual(ranking[0], "1. Tarantulas, 3 pts")  # score 3 first
        self.assertEqual(ranking[1], "2. FC Awesome, 1 pts")  # score 1 second
        self.assertEqual(ranking[2], "2. Lions, 1 pts")  # score 1 second
        self.assertEqual(ranking[3], "4. Snakes, 0 pts")  # score 0 forth


if __name__ == '__main__':
    unittest.main()