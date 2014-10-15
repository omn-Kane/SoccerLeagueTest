import argparse
import logging

logger = logging.getLogger("SoccerLeagueScores")


class SoccerLeagueScores:
    def __init__(self):
        self.file_contents = {}
        self.scores = {}

    def add_input(self, input_file):
        logger.info("Loading data from file %s" % input_file)
        self.file_contents = open(input_file).readlines()

    def calculate_scores(self):
        logger.info("Calculate Game Scores")
        for game in self.file_contents:
            game_points = self.extract_line_input(game)
            self.add_game_score(game_points)
        rankings = self.rank_scores()
        self.print_rankings(rankings)

    def extract_line_input(self, game):
        split = game.split(', ', 1)
        first_split = split[0].rsplit(' ', 1)
        second_split = split[1].rsplit(' ', 1)
        return {'first': {'name': first_split[0], 'score': int(first_split[1])}, 'second': {'name': second_split[0], 'score': int(second_split[1])}}

    def add_game_score(self, game_points):
        first_team_name = game_points['first']['name']
        second_team_name = game_points['second']['name']
        if int(game_points['first']['score']) == int(game_points['second']['score']):
            self.scores[first_team_name] = self.get_dict_for_team(first_team_name, game_points['first']['score'], 1)
            self.scores[second_team_name] = self.get_dict_for_team(second_team_name, game_points['second']['score'], 1)
        elif int(game_points['first']['score']) > int(game_points['second']['score']):
            self.scores[first_team_name] = self.get_dict_for_team(first_team_name, game_points['first']['score'], 3)
            self.scores[second_team_name] = self.get_dict_for_team(second_team_name, game_points['second']['score'], 0)
        else:
            self.scores[first_team_name] = self.get_dict_for_team(first_team_name, game_points['first']['score'], 0)
            self.scores[second_team_name] = self.get_dict_for_team(second_team_name, game_points['second']['score'], 3)

    def rank_scores(self):
        logger.debug(self.scores)
        ranking = [team for team in self.scores.values()]
        ranking = sorted(ranking, key=lambda points_sort: points_sort['points'], reverse=True)

        rankings = []
        previous_points = 0
        for loop in range(0, len(ranking)):
            rank = loop + 1
            if int(previous_points) == int(ranking[loop]['points']):
                rank -= 1
            rankings.append("%s. %s, %s pts" % (rank, ranking[loop]['name'], ranking[loop]['points']))
            previous_points = ranking[loop]['points']

        return rankings

    def print_rankings(self, rankings):
        for item in rankings:
            logger.info(item)

    def get_dict_for_team(self, team_name, team_score, team_points):
        if self.scores.get(team_name):
            current_team_points = self.scores.get(team_name).get('points')
            current_team_score = self.scores.get(team_name).get('score')
            return {'name': team_name, 'score': int(current_team_score) + int(team_score), 'points': int(current_team_points) + int(team_points)}
        else:
            logger.debug("new team: " + team_name)
            return {'name': team_name, 'score': int(team_score), 'points': int(team_points)}


def parse_arguments():
    """
    Parses the input arguments to determine the file from which to read the json data.
    """
    logger.info("Parsing input parameters")
    parse = argparse.ArgumentParser(description='Soccer League Scores')
    parse.add_argument("-f", "--file", required=False, help="The Input file with the scores of each game", default="./data/input.txt")
    parse.add_argument("-v", "--verbosity", required=False, action="count", default=0)

    return parse.parse_args()


if __name__ == '__main__':
    try:
        arguments = parse_arguments()

        # determine the log level based on the verbosity parameter
        log_level = logging.INFO
        if arguments.verbosity > 0:
            log_level = logging.DEBUG

        logging.basicConfig(format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', level=log_level)

        soccerLeagueScores = SoccerLeagueScores()
        soccerLeagueScores.add_input(input_file=arguments.file)
        soccerLeagueScores.calculate_scores()
    except KeyboardInterrupt:
        logger.info("Shutting down")
        exit()