import requests, sqlite3, datetime, time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError
from urllib3.util import Retry

def add_to_db(data, key_set, database_file):
    # This function expects as input a list of dictionaries.
    # This function adds the data inputted into it to the database.

    # Connect to the database and create a cursor.
    sqliteConnection = sqlite3.connect(database_file)
    cursor = sqliteConnection.cursor()
    
    # Loop through the entries previously collected.
    for entry in data:
        date_unix   = entry[key_set['date_unix_key']]
        date_text   = entry[key_set['date_text_key']]
        level       = entry[key_set['level_key']]
        rain_rate   = entry[key_set['rain_r_key']]
        rain_acc    = entry[key_set['rain_a_key']]
        temperature = entry[key_set['temp_key']]
        
        # Check if an entry does not already exist for that timestamp.
        # If it does not, add it.
        db_query = cursor.execute(f"SELECT * FROM entries WHERE date_unix = '{date_unix}';")
        db_query = db_query.fetchall()
        if len(db_query) == 0:
            cursor.execute(f"""INSERT INTO entries (date_unix, date_text, level, rain_rate, rain_acc, temperature) 
                        VALUES ('{date_unix}', '{date_text}', '{level}', '{rain_rate}', '{rain_acc}', '{temperature}');""")
            print(entry, " Added to the database!")
    
    # This is necessary in order to actually commit the changes.
    # This is good, otherwise the code could mess up with database if it failed.
    sqliteConnection.commit()
        
    return 0 

def get_data(key_set, safe_url):
    # Get the data from the public defense website.
    
    # I found this idea online. It helped making the accesses more stable.
    # It makes the code retry multiple times if connection fails, with increasing time between trials.
    retry_strategy = Retry(total=5, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount('https://', adapter)

    # Get the data.
    try:
        data = session.get(safe_url)
    except ConnectionError as ce:
        raise ce
    
    # Extract the data from the website.
    data = BeautifulSoup(data.content, 'html.parser')

    # Now treat the data into a list of dictionaries.
    data_collected = []
    for row in data.tbody.find_all('tr'):
        columns = row.find_all('td')
        if(columns != []):
            date        = columns[0].text.strip()
            level       = columns[1].text.strip()
            rain_rate   = columns[2].text.strip()
            rain_acc    = columns[3].text.strip()
            temperature = columns[4].text.strip()
            data_collected.append({key_set['date_unix_key'] : convert_to_unix(date),
                                   key_set['date_text_key'] : date,
                                   key_set['level_key']     : level, 
                                   key_set['rain_r_key']    : rain_rate, #(mm/h) 
                                   key_set['rain_a_key']    : rain_acc, #(mm)
                                   key_set['temp_key']      : temperature}) #(Celsius) 

    # It is necessary to invert the data order here so that the entries in the database will be correctly ordered.
    start = len(data_collected) - 1
    data_collected_reversed = [data_collected[i] for i in range(start, -1, -1)]                
    return data_collected_reversed

def get_latest_entry(database_file, key_set):
    # Returns the last entry by order of time from the databse.
    sqliteConnection = sqlite3.connect(database_file)
    cursor = sqliteConnection.cursor()
    cursor.execute(f"SELECT * FROM entries ORDER BY {key_set['date_unix_key']} DESC LIMIT 1;")
    return cursor.fetchone()

def convert_to_timestamp(unix_timestamp):
    # Converts a timestamp in day-month-year hour-minute format to unix format.
    return datetime.datetime.strptime(unix_timestamp, "%Y-%m-%d %H:%M")

def convert_to_unix(timestamp=str):
    # Converts a unix timestamp to day-month-year hour-minute format.
    timestamp_format = "%d-%m-%Y %H:%M"
    converted_timestamp = datetime.datetime.strptime(timestamp.replace("/", "-"), timestamp_format)
    return int(time.mktime(converted_timestamp.timetuple()))

def get_today():
    # Returns current date in year-month-day format.
    return (datetime.datetime.now()).strftime("%Y-%m-%d")

def get_url_for_date(start_date=get_today(), end_date=get_today()):
    # Below is the url to the government website that displays the sensor data for a specific date.
    # If no input is given, it will be filled with the current date.
    # By standard, the database is set up to work with 30 minute intervals. 
    # If desired, intervalo can be adjusted between 5, 15, 30 or 60 in order to adjust intervals between readings.
    # I highly suggest NOT mixing intervals in the same table.
    url_mod = f'''https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem-sensores
    &_tog1149016d=all
    &_pjax=%23kv-pjax-container-metragem-sensores
    &DreikSearch[data_inicial]={start_date}
    &DreikSearch[data_final]={end_date}
    &DreikSearch[intervalo]=30
    &DreikSearch[ordenacao]=3'''
    url_mod = url_mod.replace("\n","")
    url_mod = url_mod.replace(" ","")
    return url_mod

def date_set_builder(year):
    # This function returns a list with dates that can be used in conjunction with the
    # get_url_for_date function in order to create several accesses to populate the db.
    start_date = datetime.datetime(year, 1, 1)
    end_date   = datetime.datetime(year + 1, 1, 1)
    delta      = datetime.timedelta(days=1)
    
    iteration  = start_date
    whole_year = []
    
    while iteration < end_date:
        whole_year.append(iteration.strftime("%Y-%m-%d"))
        iteration += delta
        
    return whole_year

def get_database_variables():
    # This function return the column names from the database, and the db file name.
    # I found this useful because it makes modifying the code easier, if necessary.
    database_file = 'rain_data.db'
    key_set = {
    'date_unix_key' : 'Date_unix',
    'date_text_key' : 'Date_text',
    'level_key'     : 'Level', 
    'rain_r_key'    : 'Rain_rate', 
    'rain_a_key'    : 'Rain_acc', 
    'temp_key'      : 'Temperature'
    }
    
    return database_file, key_set

def build_message(entry):
    # This function checks the data given to it and generates a respective message.
    # Entry must be a list of values, and values must be ordered as especified in the code below.
    
    # These values come from experience.
    ximbica_bridge_level = 4  # At this height, the bridge starts to flood. Measure in meters.
    ximbica_flood_level = 5.3  # At this height, the bride is no longer traversable. Measure in meters.
    ximbica_flood_rain_rate = 20.0  # Measure in mm/h.
    
    # Get the respective values from the entry from the database.
    timestamp = entry[2]
    level = entry[3]
    rain_rate = entry[4]
    
    # Return a status value in order to choose the type of message to return.
    if float(level) >= ximbica_flood_level:
        status = 2
    elif float(level) >= ximbica_bridge_level and float(level) <= ximbica_flood_level:
        status = 3
    elif float(level) <= ximbica_flood_level and float(rain_rate) >= ximbica_flood_rain_rate:
        status = 1
    else:
        status = 0
    
    # Build the message. I create it as a list so I can join it later and make the code tidier.
    message = []
    message.append(f"Current time: {timestamp}.")
    message.append(f"Current river level: {level} m.")
    message.append(f"Current rain rate: {rain_rate} mm/h.")
    
    # Since there's no sensor specifically at the bridge, the messages are worded as possibilities.
    if status == 0:
        message.append(f"Given current sensor data, Ximbica is most likely not flooded.")
        message.append(f"The bridge is almost certainly traversable.")
    if status == 1:
        message.append(f"Given current sensor data, Ximbica may be flooded, due to heavy rain.")
        message.append(f"The bridge may not be traversable.")
    if status == 2:
        message.append(f"Given current sensor data, Ximbica is likely flooded.")
        message.append(f"The bridge is almost certainly not be traversable.")
    if status == 3:
        message.append(f"Given current sensor data, Ximbica may be flooded.")
        message.append(f"The bridge may still be traversable however. Proceed at your own risk.")
    return '\n'.join(message)