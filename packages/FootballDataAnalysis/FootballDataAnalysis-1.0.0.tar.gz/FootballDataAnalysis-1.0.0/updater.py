import hidden
import http.client
import json

def updater(league):

    connection = http.client.HTTPConnection('api.football-data.org')
    headers = {'X-Auth-Token': hidden.token, 'X-Response-Control': 'minified'}
    connection.request('GET', '/v2/competitions/' + league + '/teams', None, headers)
    teams = json.loads(connection.getresponse().read().decode())
    with open("data/"+league + "teams.json", 'w', encoding='utf-8') as results:
        json.dump(teams, results)
    # Standings
    connection.request('GET', '/v2/competitions/' + league + '/standings', None, headers)
    teams = json.loads(connection.getresponse().read().decode())
    with open("data/" + league + "standings.json", 'w', encoding='utf-8') as results:
        json.dump(teams, results)
    # Scorers
    connection.request('GET', '/v2/competitions/' + league + '/scorers', None, headers)
    teams = json.loads(connection.getresponse().read().decode())
    with open("data/" + league + "scorers.json", 'w', encoding='utf-8') as results:
        json.dump(teams, results)
    # Matches
    connection.request('GET', '/v2/competitions/' + league + '/matches', None, headers)
    teams = json.loads(connection.getresponse().read().decode())
    with open("data/" + league + "matches.json", 'w', encoding='utf-8') as results:
        json.dump(teams, results)


#updater("PD")
#updater("FL1")
#updater("BL1")
#updater("PL")
#updater("SA")

