import data_tools

# The website allows for access to data per 3 days only.
database_file, key_set = data_tools.get_database_variables()
test_set = data_tools.date_set_builder(2021)
step = 2
i = 0

for index, day in enumerate(test_set):
    try:
        if i == 0:
            url_input = data_tools.get_url_for_date(test_set[index], test_set[index + step])
            data_for_day = data_tools.get_data(key_set, url_input)
            data_tools.add_to_db(data_for_day, key_set, database_file)
            i += 1
        elif i > 0 and i < step:
            i += 1
        else:
            i = 0
    except IndexError:
        url_input = data_tools.get_url_for_date(test_set[index], test_set[index])
        data_for_day = data_tools.get_data(key_set, url_input)
        data_tools.add_to_db(data_for_day, key_set, database_file)