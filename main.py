import data_tools as dt
import twitter_helpers as th
import time, logging

while True:
    try:
        url = dt.get_url_for_date()
        db_file, key_set = dt.get_database_variables()
        today_data = dt.get_data(key_set, url)
        dt.add_to_db(today_data, key_set, db_file)
        latest_entry = dt.get_latest_entry(db_file, key_set)
        print(latest_entry)
        message = dt.build_message(latest_entry)
        th.tweet(message)

        time.sleep(3600)
    
    except Exception as e:
        print("An error has occurred: ", e)
        print("Please check what happened. Bot will shutdown now.")
        break