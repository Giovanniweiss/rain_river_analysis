import data_tools, sqlite3, datetime

# Command to get the data I want from the database.
database_file, key_set = data_tools.get_database_variables()
sqliteConnection = sqlite3.connect(database_file)
cursor = sqliteConnection.cursor()

start_date = data_tools.convert_to_unix((datetime.datetime(2023, 1, 1, 0, 0)).strftime("%d-%m-%Y %H:%M"))
end_date = data_tools.convert_to_unix((datetime.datetime(2023, 12, 31, 23, 59)).strftime("%d-%m-%Y %H:%M"))

column_names = list(key_set.values())
data = {}

for key in column_names:
    db_query = cursor.execute(f"SELECT {key} FROM entries WHERE {key_set['date_unix_key']} > '{start_date}' AND {key_set['date_unix_key']} < '{end_date}';")
    data[key] = cursor.fetchall()

# Command to plot the data onto a graph.
