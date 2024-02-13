# Ximbica river depth reporter
#### Video demo: link to the video once it is recorded.


## Description
This is a project developed by Giovanni Francisco Weiss as the final project for Harvard University's CS50x 2024.  
It is a Twitter bot, written mostly in Python, that will check the website of the *Defesa Civil de Rio do Sul* and post updates regarding the traversable status of a particularly badly located bridge.  
When the script is executed, the bot will scrape the latest sensor data from the government's website and perform a check based on that data, from which it is possible to infer if the bridge is still traversable on foot or with a land vehicle. For convenience, it will then post this status into a Twitter account, with a brief overview of the current situation.  
Deeper data analysis was not the focus of this project. However, data collected is stored into the file *rain_data.db*, and there are functions in the project that can be used to extract historical data, so further work could be done in this area.


## Files in this project
* **data_tools.py**  
Contains functions used to access, scrape, store and process data from the govenment website.
* **twitter_helper.py**  
Contains functions that authenticate and post a tweet containing a message. They are useless without a file named API_access_tokens.txt  
* **API_access_tokens.txt**  
This file is not included in the github copy of this project because I will not share my twitter API access codes. However, should you wish to use this project for something, you need to make this file yourself. Format it as especified in the twitter_helper.py  
* **db_schema.sql**  
This file contains the database schema, in case the database file is ever lost.
* **rain_data.db**  
This is a sqlite3 database containing all the data the bot collects.
* **populate_database.py**  
This is a separate script which can be used to collect historical data from the government website.
* **main.py**  
This is the main script file. Running this file will start a python program that will run the bot indefinitely, checking for new data every hour.

## Further Context
The city of Rio do Sul has a remarkable location in the state of Santa Catarina, Brazil, as in the heart of the city, two rivers join and form the Rio Itajaí-Açu, a major river which flows more than 270km down the state until it reaches the atlantic ocean.  
This river was paramount to the settling of the land by european migrants in the 19th and 20th century, as it allowed for easy transportation of wood down to the coast.  
The location of Rio do Sul, however, is also threatened by its landscape. When it rains, the water from the whole region of the Alto Vale do Itajaí, flows into the Itajaí-Açu. The river, in turn, is not wide enough to keep up with the downpour at times, and flooding occurs.  
As of February of 2024, the time of writing this file, the author of this project himself has lived through 10 separate floods, of varying intensities, after living for 3 years in this city. In November 2023, Rio do Sul faced its second worst flood since 1911 as the river rose 11 meters above its normal measument, in a matter of 12 hours. This was a major blow to the local economy, which, as of the time of writing this file, is still far from recovering.  
The Ximbica bridge, the point of interest in this project, is a very small but very important, 10 meter long bridge that connects a major quarter to the highway and to the city center. However, it is also located in perhaps the lowest point of the city - so much so that localized heavy rain will cause it to flood in a matter of minutes, much to the inconvenience of everyone who uses it frequently - the author included - hence the point of this project.