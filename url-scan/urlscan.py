import requests
import json
import config_file


def get_quotas():
    url = config_file.quotas_url
    headers = {"Content-Type": "application/json", "API-Key": config_file.api_key}
    try:
        response = requests.get(url, headers=headers)
        data_string = response.content.decode('utf-8')
        data_obj = json.loads(data_string)
        search_quotas = {key: value['remaining'] for (key, value) in data_obj['limits']['search'].items()}
    except Exception as e:
        print(e.__class__)

    return search_quotas


def search_scans_by_query(query, search_data):
    quotas = get_quotas()
    url = config_file.search_url
    headers = {"Content-Type": "application/json", "API-Key": config_file.api_key}
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

