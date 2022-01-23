import alert_priority_map
import alerts_input


class AlertPicker:
    def __init__(self):
        self.type_subtype_map = dict()
        self.create_type_subtype_map()

    def create_type_subtype_map(self):
        for k, v in alert_priority_map.priority_map.items():
            for i in range(len(v)):
                self.type_subtype_map[v[i]['alert_type'] + v[i]['alert_subtype']] = [k, v[i]['title_identifiers']]

    def alerts_cherry_picking(self):
        alerts_ids = []
        sorted_alerts = sorted(alerts_input.alerts, key=self.sort_key_function, reverse=True)
        for alert in sorted_alerts:
            if self.search_title_identifiers(alert):
                alerts_ids.append(alert['_id'])
            if len(alerts_ids) >= 4:
                break
        return alerts_ids

    def search_title_identifiers(self, alert):
        alert_type_str = alert['Details']['Type'] + alert['Details']['SubType']
        title_identifiers = self.type_subtype_map[alert_type_str][1]
        for title in title_identifiers:
            if title in alert['Title']:
                return True
        return False

    def sort_key_function(self, alert):
        # lower priority score comes first, also newer dates come first.
        # we'll take key=(-priority, date), and sort in reverse, so that the biggest value has the lowest priority score
        alert_priority = self.type_subtype_map[alert['Details']['Type'] + alert['Details']['SubType']][0]
        return -alert_priority, alert['FoundDate']
