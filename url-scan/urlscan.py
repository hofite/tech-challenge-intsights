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


def search_scans_by_query(query, res_data):
    url = config_file.search_url
    headers = {"Content-Type": "application/json", "API-Key": config_file.api_key}
    payload = {'q': query, 'size': 10000, 'search_after': None}

    try:
        while True:
            response = requests.get(url, params=payload, headers=headers)
            data_string = response.content.decode('utf-8')
            data_obj = json.loads(data_string)
            total = data_obj['total']

            res_data.extend(data_convert(data_obj))

            if len(res_data) >= total:
                break
            else:
                a = ','.join(str(x) for x in data_obj['results'][-1]['sort'])
                payload['search_after'] = a

    except Exception as e:
        print(e.__class__)

    return res_data


def data_convert(obj):
    return [{'page_url': res['page']['url'], 'page_screenshot': res['screenshot']} for res in obj['results']]
