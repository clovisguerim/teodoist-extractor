import todoist_extractor.todoist_extractor as todex
from dotenv import load_dotenv, dotenv_values
import pandas as pd
from glob import glob
import os
from datetime import date, datetime, timedelta


def get_min_diff_date_from_today(list_of_dates):
    diff_dates = {
        datetime.today() - datetime.strptime(d, "%Y%m%d"): d
        for d in list_of_dates
    }
    min_diff = min(list(diff_dates.keys()))
    return diff_dates[min_diff]


def run(update=True):

    credentials = dotenv_values('../.env')
    path_data = "../data/"
    glob_search = f"{path_data}*.csv"

    te = todex.TodoistExtractor(
        token=credentials["TOKEN"],
        pages=5,
        limit=100
    )
    df = te.get_todoist_activities()
    df['content'] = df['extra_data'].apply(lambda x: x['content'] if 'content' in x.keys() else None)
    df['due_date'] = df['extra_data'].apply(lambda x: x['due_date'] if 'due_date' in x.keys() else None)
    df['name'] = df['extra_data'].apply(lambda x: x['name'] if 'name' in x.keys() else None)
    object_id_list = [te.get_parent_id(idd) for idd in df['object_id'].unique()]
    parent_id_dp = pd.DataFrame([object_id_list, df['object_id'].unique()]).T
    parent_id_dp = parent_id_dp.rename(columns={0: 'parent_id', 1: 'object_id'}).astype(int, errors='ignore')
    df = df.merge(parent_id_dp, on='object_id')

    if update:

        max_dates_on_folder = [
            d.split("/")[-1].split('-')[-1].split('.')[0] for d in glob(glob_search)
        ]
        current_state_date = get_min_diff_date_from_today(max_dates_on_folder)

        df['event_date_formatted'] = pd.to_datetime(
            df['event_date'], infer_datetime_format=True
        ).dt.strftime("%Y%m%d")
        df_new = df[df['event_date_formatted'] >= current_state_date]
        dates_to_save_file = df_new['event_date_formatted'].min(), df_new['event_date_formatted'].max()

        file_name = f"TODOIST-{dates_to_save_file[0]}-{dates_to_save_file[1]}.csv"

        print(file_name)

        df_new = df_new.drop('event_date_formatted', axis=1)
        df_new.to_csv(os.path.join(path_data, file_name), index=False)
    else:

        df['event_date_formatted'] = pd.to_datetime(
            df['event_date'], infer_datetime_format=True
        ).dt.strftime("%Y%m%d")
        dates_to_save_file = df['event_date_formatted'].min(), df['event_date_formatted'].max()
        file_name = f"TODOIST-{dates_to_save_file[0]}-{dates_to_save_file[1]}.csv"
        df.to_csv(os.path.join(path_data, file_name), index=False)


if __name__ == "__main__":
    run()
