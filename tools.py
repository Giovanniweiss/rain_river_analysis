import requests, sqlite3, datetime, time
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, parse_qsl, urlencode, urlunparse

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
    # Extract the data from the website.
    data = requests.get(safe_url)
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

    # Connection seems to fail a lot, so add an except for that.     

    # It is necessary to invert the data order here so that the entries in the database will be correctly ordered.
    start = len(data_collected) - 1
    data_collected_reversed = [data_collected[i] for i in range(start, -1, -1)]                
    return data_collected_reversed

def convert_to_timestamp(unix_timestamp):
    return datetime.datetime.strptime(unix_timestamp, "%Y-%m-%d %H:%M")

def convert_to_unix(timestamp=str):
    timestamp_format = "%d-%m-%Y %H:%M"
    converted_timestamp = datetime.datetime.strptime(timestamp.replace("/", "-"), timestamp_format)
    return int(time.mktime(converted_timestamp.timetuple()))

def get_url_for_date(start_date, end_date):
    url_mod = f'''https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem-sensores&_tog1149016d=all&_pjax=%23
                  kv-pjax-container-metragem-sensores&
                  DreikSearch[data_inicial]={start_date}&
                  DreikSearch[data_final]={end_date}&
                  DreikSearch[intervalo]=30&
                  DreikSearch[ordenacao]=3
                  '''
    parsed_url = urlparse(url_mod)
    params = dict(parse_qsl(parsed_url.query))
    encoded_params = {k: quote(v) for k, v in params.items()}
    parsed_url = parsed_url._replace(query=urlencode(encoded_params))
    safe_url = urlunparse(parsed_url)
    safe_url = url_mod
    return safe_url.replace("\n","")

def date_set_builder(year):
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
    database_file = 'rain_data.db'
    key_set = {
    'date_unix_key' : 'Date_unix',
    'date_text_key' : 'Date_text',
    'level_key'     : 'Level', 
    'rain_r_key'    : 'Rain_rate', 
    'rain_a_key'    : 'Rain_acc', 
    'temp_key'      : 'Temperature'
    }
    
    return database_file,key_set
