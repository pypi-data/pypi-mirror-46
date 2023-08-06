class MatchList(list):

    def get_matchday(self, num):
        """
        Return all matches of given matchday
        :param num: matchday number
        :return: MatchList object containing all matches of given matchday
        """
        matchday = []
        for el in self:
            if el[1] == num:
                matchday.append(el)
        return MatchList(matchday)

    def get_team_matches(self, team_name):
        """
        Return all team matches
        :param team_name: name of the team
        :return: MatchList object containing all matches of given team
        """
        team_matches = []
        for el in self:
            if el[2] == team_name or el[3] == team_name:
                team_matches.append(el)
        return MatchList(team_matches)

    def get_home_matches(self, team_name):
        """
        Return all team home matches
        :param team_name: name of the team
        :return: MatchList object containing all home matches of given team
        """
        home_matches = []
        for el in self.get_team_matches(team_name):
            if el[2] == team_name:
                home_matches.append(el)
        return MatchList(home_matches)

    def get_away_matches(self, team_name):
        """
        Return all team away matches
        :param team_name: name of the team
        :return: MatchList object containing all away matches of given team
        """
        away_matches = []
        for el in self.get_team_matches(team_name):
            if el[3] == team_name:
                away_matches.append(el)
        return MatchList(away_matches)

    def get_stats(self, team_name):
        """
        Return wins, draws and loses statistics
        :param team_name: name of the team
        :return: tuple containing 4 values(games played, wins, draws, loses)
        """
        wins = 0
        loses = 0
        draws = 0
        for el in self.get_home_matches(team_name):
            if el[0] == "FINISHED":
                if el[4]['homeTeam'] > el[4]['awayTeam']:
                    wins += 1
                elif el[4]['homeTeam'] == el[4]['awayTeam']:
                    draws += 1
                else:
                    loses += 1
        for el in self.get_away_matches(team_name):
            if el[0] == "FINISHED":
                if el[4]['homeTeam'] > el[4]['awayTeam']:
                    loses += 1
                elif el[4]['homeTeam'] == el[4]['awayTeam']:
                    draws += 1
                else:
                    wins += 1
        games = wins + draws + loses
        return (games, wins, draws, loses)

    def get_goals(self, team_name):
        """
        Return scored and conceded goals
        :param team_name: name of the team
        :return: tuple with 2 values (goals scored, goals missed)
        """
        scored = 0
        missed = 0
        for el in self.get_home_matches(team_name):
            if el[0] == "FINISHED":
                scored += el[4]['homeTeam'] 
                missed += el[4]['awayTeam']
        for el in self.get_away_matches(team_name):
            if el[0] == "FINISHED":
                scored += el[4]['awayTeam']
                missed += el[4]['homeTeam']
        return(scored, missed)
