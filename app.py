import requests, sqlite3, re
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qsl, urlencode, urlunparse

def is_ximbica_flooded(level):
    ximbica_flood_level = 5.3
    if float(level) > ximbica_flood_level:
        return True
    else:
        return False

def add_to_db(data, key_set, database_file):
    # This function expects as input a list of dictionaries.
    # This function adds the data inputted into it to the database.

    # Connect to the database and create a cursor.
    sqliteConnection = sqlite3.connect(database_file)
    cursor = sqliteConnection.cursor()
    
    # Loop through the entries previously collected.
    for entry in data:
        date        = entry[key_set['date_key']]
        time        = entry[key_set['time_key']]
        level       = entry[key_set['level_key']]
        rain_rate   = entry[key_set['rain_r_key']]
        rain_acc    = entry[key_set['rain_a_key']]
        temperature = entry[key_set['temp_key']]
        
        # Check if an entry does not already exist for that timestamp.
        # If it does not, add it.
        db_query = cursor.execute(f"SELECT * FROM entries WHERE date = '{date}' AND time = '{time}';")
        db_query = db_query.fetchall()
        if len(db_query) == 0:
            cursor.execute(f"""INSERT INTO entries (date, time, level, rain_rate, rain_acc, temperature) 
                        VALUES ('{date}', '{time}', '{level}', '{rain_rate}', '{rain_acc}', '{temperature}');""")
            print(entry, " Added to the database!")
    
    # This is necessary in order to actually commit the changes.
    # This is good, otherwise the code could mess up with database if it failed.
    sqliteConnection.commit()
        
    return 0 

def get_data(key_set):
    # Get the data from the public defense website.
    try:
        # The code below was suggest by CS50.ai in order to encode my url.
        url = "https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem-sensores&_tog1149016d=all&_pjax=%23kv-pjax-container-metragem-sensores&DreikSearch[intervalo]=5"
        parsed_url = urlparse(url)
        params = dict(parse_qsl(parsed_url.query))
        encoded_params = {k: quote(v) for k, v in params.items()}
        parsed_url = parsed_url._replace(query=urlencode(encoded_params))
        safe_url = urlunparse(parsed_url)

        # Extract the data from the website.
        data = requests.get(safe_url)
        data = BeautifulSoup(data.content, 'html.parser')
        
        # Patterns for locating time and date.
        date_regex = re.compile(r'\d\d/\d\d/\d\d\d\d')
        time_regex = re.compile(r'\d\d:\d\d')

        # Now treat the data into a list of dictionaries.
        data_collected = []
        for row in data.tbody.find_all('tr'):
            columns = row.find_all('td')
            if(columns != []):
                temp        = columns[0].text.strip()
                date        = date_regex.search(temp).group()
                time        = time_regex.search(temp).group()
                level       = columns[1].text.strip()
                rain_rate   = columns[2].text.strip()
                rain_acc    = columns[3].text.strip()
                temperature = columns[4].text.strip()
                data_collected.append({key_set['date_key']   : date, 
                           key_set['time_key']   : time,
                           key_set['level_key']  : level, 
                           key_set['rain_r_key'] : rain_rate, #(mm/h) 
                           key_set['rain_a_key'] : rain_acc, #(mm)
                           key_set['temp_key']   : temperature}) #(Celsius) 

    # Connection seems to fail a lot, so add an except for that.     
    except:
        return 1

    # It is necessary to invert the data order here so that the entries in the database will be correctly ordered.
    start = len(data_collected) - 1
    data_collected_reversed = [data_collected[i] for i in range(start, -1, -1)]                
    return data_collected_reversed


database_file = 'rain_data.db'
key_set = {
    'date_key'   : 'Date', 
    'time_key'   : 'Time',
    'level_key'  : 'Level', 
    'rain_r_key' : 'Rain_rate', 
    'rain_a_key' : 'Rain_acc', 
    'temp_key'   : 'Temperature'
}

rain_data = (get_data(key_set))
add_to_db(rain_data, key_set, database_file)

# After we have the data, it's time to work on checking if the bridge is passable.
# Get the latest data entry from the database.

sqliteConnection = sqlite3.connect(database_file)
cursor = sqliteConnection.cursor()

db_query = cursor.execute(f"SELECT * FROM entries ORDER BY id DESC LIMIT 1;")
latest_entry = cursor.fetchone()
if is_ximbica_flooded(latest_entry[3]):
    print("It's flooded!!")
else:
    print("All is well in Ximbica.")
    
