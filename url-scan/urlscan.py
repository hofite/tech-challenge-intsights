import requests
import json


def get_quotas():
    url = "https://urlscan.io/user/quotas/"
    headers = {"Content-Type": "application/json", "API-Key": "0e55a0ee-2ec5-4db0-a713-409aefdb3790"}
    try:
        response = requests.get(url, headers=headers)
        data_string = response.content.decode('utf-8')
        data_obj = json.loads(data_string)
        search_quotas = {key: value['remaining'] for (key, value) in data_obj['limits']['search'].items()}
    except Exception as e:
        print(e.__class__)

    return search_quotas


# domain:tines.io  OR yyi1i.co - query input example
def search_scans_by_query(query, search_data):
    quotas = get_quotas()
    url = "https://urlscan.io/api/v1/search/"
    headers = {"Content-Type": "application/json", "API-Key": "0e55a0ee-2ec5-4db0-a713-409aefdb3790"}
    payload = {'q': query, 'size': 10000, 'search_after': None}

    if quotas['day'] <= 0 or quotas['hour'] <= 0 or quotas['minute'] <= 0:
        print("You have exceeded your limit: query " + query + " is not executed")
        return

    try:
        while True:
            response = requests.get(url, params=payload, headers=headers)
            data_string = response.content.decode('utf-8')
            data_obj = json.loads(data_string)
            total = data_obj['total']

            search_data.extend(data_convert(data_obj))

            if len(search_data) >= total:
                break
            else:
                a = ','.join(str(x) for x in data_obj['results'][-1]['sort'])
                payload['search_after'] = a

    except Exception as e:
        print(e.__class__)

    return


def data_convert(obj):
    return [{'page_url': res['page']['url'], 'page_screenshot': res['screenshot']} for res in obj['results']]


