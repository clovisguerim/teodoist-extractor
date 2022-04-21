from todoist import TodoistAPI
import pandas as pd


class TodoistExtractor:

    def __init__(self, token, pages, limit):
        self.token = token
        self.api = TodoistAPI(self.token)
        self.api.sync()
        self.pages = pages
        self.limit = limit

    def get_todoist_activities(self):
        activities = pd.DataFrame()
        all_activities = []
        for p in range(self.pages):
            if p > 0:
                activities = all_activities
            activities_on_page_df = pd.DataFrame(self.api.activity.get(page=p, limit=self.limit)['events'])
            all_activities = pd.concat([activities, activities_on_page_df])
        return all_activities

    def get_parent_id(self, object_id):
        object_id = str(object_id)
        info_list = [self.api.items.get_by_id(object_id)]
        for item in info_list:
            try:
                if ('item' in item.keys()) and ('parent_id' in item['item'].keys()):
                    return item['item']['parent_id']
            except AttributeError:
                return None