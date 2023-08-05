import json
from datetime import datetime
from requests import Session

from cog_nba.settings import USER_AGENT, MAX_CACHE_AGE
from cog_nba.database import DBConnection, Query


def construct_url(endpoint):
    # Construct URL based on endpoint name.
    # https://github.com/seemethere/nba_py/wiki/stats.nba.com-Endpoint-Documentation
    # Documentation states https://stat.nba.com/stats/<endpoint>/?<params>

    url = 'https://stats.nba.com/stats/%s' % endpoint

    return url


def get(endpoint, *args):
    # Base function for the other functions in this wrapper.
    # Requires endpoint as str and params as dict.

    if type(endpoint) != str:
        raise Exception('Endpoint not a string.')

    payload = {}
    for arg in args:
        if type(arg) != dict:
            raise Exception('Invalid parameter passed, should be dict.')
        else:
            payload.update(arg)

    if check_database(endpoint, json.dumps(payload)):
        # If recent record is found, then return data from SQL rather than excute GET.
        with DBConnection() as db:
            query = db.session.query(Query).filter_by(endpoint=endpoint, params=json.dumps(payload)).first()
            db.session.close()
            return json.loads(query.data)

    else:
        # Rotate user agent and IPs to avoid being blocked
        # TODO: Build in proxies into the GET function.

        headers = {
            'host': 'stats.nba.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'connection': 'keep-alive',
            'user-agent': USER_AGENT,
        }

        url = construct_url(endpoint)

        with Session() as session:
            response = session.get(url, params=payload, headers=headers)

        store_response(endpoint, payload, response)

        return response.json()


def check_database(endpoint, params):
    # Checks table for existing record, and checks how old that record is.
    # MAX_CACHE_AGE can be set in settings

    with DBConnection() as db:
        query = db.session.query(Query).filter_by(endpoint=endpoint, params=params)
        db.session.close()

    if query.scalar():
        if (datetime.utcnow() - query.first().date).days > MAX_CACHE_AGE:
            return False
        else:
            return True
    else:
        return False


def store_response(endpoint, params, response):
    # Store the JSON data captured from the request into a table.
    # Note, params and data should be called with json.dumps() when comparing in check_database().

    response = response.json()

    query = Query(
        endpoint=endpoint,
        params=json.dumps(params),
        data=json.dumps(response)
    )

    with DBConnection() as db:
        try:
            db.session.add(query)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(getattr(e, 'message', repr(e)))


def get_current_players():
    # Shortcut function to get all current players.

    params = {
        'LeagueID': '00',
        'Season': '2018-19',
        'IsOnlyCurrentSeason': '1'
    }

    response = get('commonallplayers', params)

    return response


def get_all_players():
    # Shortcut function to get all players.

    params = {
        'LeagueID': '00',
        'Season': '2018-19',
        'IsOnlyCurrentSeason': '0'
    }

    response = get('commonallplayers', params)

    return response


def get_player_career_stats(player_id, metric):
    # Get player stats, metric should be 'Totals', 'PerGame', 'Per36'

    if str(metric) not in ['Totals', 'PerGame', 'Per36']:
        raise Exception('Metric should be "Totals", "PerGame" or "Per36".')

    try:
        int(player_id)
    except ValueError:
        raise Exception('Player ID is not valid, needs to be a number.')

    params = {
        'PerMode': metric,
        'PlayerID': player_id
    }

    response = get('playercareerstats', params)

    return response
