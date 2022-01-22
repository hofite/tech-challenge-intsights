import datetime
import functools
import re
import utils

type_subtype_map = dict()  # a map from type+subtype to [priority, title_identifiers]


def alerts_cherry_picking(alerts):
    alerts_ids = []
    create_type_subtype_map()
    sorted_alerts = sorted(alerts, key=functools.cmp_to_key(sort_func))
    for alert in sorted_alerts:
        if search_title_identifiers(alert) and len(alerts_ids) < 4:
            alerts_ids.append(alert['_id'])
    return alerts_ids


def search_title_identifiers(alert):
    alert_type_str = alert['Details']['Type'] + alert['Details']['SubType']  # type + subtype concat
    title_identifiers = type_subtype_map[alert_type_str][1]
    for title in title_identifiers:
        if re.search(title, alert['Title']):
            return True
    return False


def create_type_subtype_map():
    for k, v in utils.priority_map.items():
        for i in range(len(v)):
            type_subtype_map[v[i]['alert_type'] + v[i]['alert_subtype']] = [k, v[i]['title_identifiers']]


def str_to_date(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%dT%X.%fZ')


def sort_func(a, b):
    a_type_str = a['Details']['Type'] + a['Details']['SubType']  # type + subtype concat
    b_type_str = b['Details']['Type'] + b['Details']['SubType']
    if a_type_str == b_type_str:
        if str_to_date(a['FoundDate']) > str_to_date(b['FoundDate']):
            return -1
        else:
            return 1
    elif type_subtype_map[a_type_str][0] > type_subtype_map[b_type_str][0]:
        return 1
    else:
        return -1
