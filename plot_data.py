import data_tools as dt
import sqlite3, datetime
import matplotlib.pyplot as plt

# Command to get the data I want from the database.
database_file, key_set = dt.get_database_variables()
sqliteConnection = sqlite3.connect(database_file)
cursor = sqliteConnection.cursor()

# These two variables se the start and end data for the graph.
start_date = dt.convert_to_unix((datetime.datetime(2023, 1, 1, 0, 0)).strftime("%d-%m-%Y %H:%M"))
end_date = dt.convert_to_unix((datetime.datetime(2023, 12, 31, 23, 59)).strftime("%d-%m-%Y %H:%M"))

# Get the column names for the database.
column_names = list(key_set.values())

data = {}
for key in column_names:
    db_query = cursor.execute(f"SELECT {key} FROM entries WHERE {key_set['date_unix_key']} > '{start_date}' AND {key_set['date_unix_key']} < '{end_date}';")
    data[key] = cursor.fetchall()
    data[key] = [i[0] for i in data[key]]

# Data selected comes as string, so convert it to float.
data[key_set['level_key']] = [float(i) for i in data[key_set['level_key']]]

# Command to plot the data onto a graph.
plt.plot(data[key_set['date_unix_key']], data[key_set['level_key']])
plt.show()