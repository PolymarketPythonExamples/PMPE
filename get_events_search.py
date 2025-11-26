import requests

def public_search(q):
    # Learn more : https://docs.polymarket.com/api-reference/search/search-markets-events-and-profiles
    # Response example: responses\gamma-api\public-search.json

    url = 'https://gamma-api.polymarket.com/public-search'
    params = {
        "q": q,
        "optimized": "true",
        "limit_per_type": 6,       # limit the number of items for each type (events, tags, profiles)
        #"type": "events",
        #"search_tags": "true",    # search for the keyword among tags
        #"search_profiles": "true" # search for the keyword among user profiles
    }    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_event(id):
    # Lear more: https://docs.polymarket.com/api-reference/events/get-event-by-id
    # Response example: responses\gamma-api\event_by_id.json

    url = f'https://gamma-api.polymarket.com/events/{id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    result = public_search('Trump')
    print(result)

    event = get_event('23085')
    print(event)