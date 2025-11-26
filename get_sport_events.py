import datetime
import json
import requests

def get_sports():
    # Learn more: https://docs.polymarket.com/api-reference/sports/get-sports-metadata-information
    # Response example: responses\gamma-api\sports.json

    url = 'https://gamma-api.polymarket.com/sports'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()    


def get_series_summary(series):
    # Learn more: 
    # Response example: responses\gamma-api\series-summary_nba.json

    url = f'https://gamma-api.polymarket.com/series-summary/{series}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json() 


def get_events(series, week):
    # Learn more: https://docs.polymarket.com/api-reference/events/list-events
    # Response example: responses\gamma-api\events_by_series_and_week.json

    url = 'https://gamma-api.polymarket.com/events'
    params = {
        "series_id" : series,
        "event_week" : week,        
        "active" : True,
        "closed" : False,
        "archived" : False,
        "end_date_min" : datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    }    
    response = requests.get(url, params=params)  
    response.raise_for_status()
    return response.json()      


if __name__ == '__main__':
    sports = get_sports()
    for sport in sports:
        print(f'{sport['sport']:<20} {sport['series']:>6} {sport['tags'].split(",")}')

    NBA_SERIES = 10345 # NBA 2025-2026 season
    NBA_WEEK = 3 # NBA earliest open week

    summary = get_series_summary(NBA_SERIES) 
    summary = json.dumps(summary, indent=4)
    print(summary)

    events = get_events(NBA_SERIES, NBA_WEEK)
    for event in events:
        for market in event['markets']:
            if market['sportsMarketType'] != "moneyline" : continue
            gameStartTime = market['gameStartTime']
            condition_id = market['conditionId']
            question = market['question']
            outcomes = json.loads(market['outcomes'])
            tokens = json.loads(market['clobTokenIds'])
            print(f'{gameStartTime} {question:<20} {condition_id} {outcomes[0]:<10} {tokens[0]} {outcomes[1]:<10} {tokens[1]}')