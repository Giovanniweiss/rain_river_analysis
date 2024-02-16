# Ximbica river depth reporter
#### Video demo: link to the video once it is recorded.


## Description
This is a project developed by Giovanni Francisco Weiss as the final project for Harvard University's CS50x 2024.  
It is a Twitter bot, written mostly in Python, that will check the website of the *Defesa Civil de Rio do Sul* and post updates regarding the traversable status of a particularly badly located bridge.  
When the script is executed through main.py, the bot will scrape the latest sensor data from the government's website upon execution and after every hour, and perform a check based on that data, from which it is possible to infer if the bridge is still traversable on foot or with a land vehicle. For convenience, it will then post this status into a Twitter account, with a brief overview of the current situation.  
Honestly, the best method for doing this would have been installing an actual water sensor on the bridge and getting the data from that, as the sensor data provided by the government comes from another bridge about 100 meters away, but I do not have that equipment, and I know from experience that flooding can be reliably interpreted through this data as written in the code.  
Deeper data analysis was not the focus of this project due to time constraints. However, data collected is stored into the file *rain_data.db*, and there are functions in the project that can be used to extract historical data, so further work could be done in this area, should I, or someone else, ever revisit it.


## Files in this project
* **data_tools.py**  
Contains functions used to access, scrape, store and process data from the government website. By itself, it does nothing, but when imported, it provides functions for creating a custom URL, getting the data from that URL, building a message to post to Twitter, and many other functions for internal use. Overall, it's the core of the project. I have written a function here that contains the database file name and schema so that it could be easily updated throughout the code, if necessary.
* **twitter_helper.py**  
Contains functions that authenticate and post a tweet containing a message. I chose to work with Tweepy as the library to use the Twitter API as it was suggested by the CS50 AI. The functions in this file are useless without a file named *API_access_tokens.txt* that contains the API client and secret codes.
* **API_access_tokens.txt**  
This file is not included in the github copy of this project because I will not share my twitter API access codes. I use it for safely storing these codes, which I then retrieve into a dictionary using a function inside *twitter_helper*. It is a simple text file containing some values, as specified below:
    * access_token:value
    * access_token_secret:value
    * consumer_key:value
    * consumer_secret:value
    * bearer_token:value  
* **db_schema.sql**  
This file contains the database schema, in case the database file is ever lost. It contains a single table, called entries, and columns for each of the values scraped from the website, plus a column for date in unix format. This column is solely for a function in data_tools to ensure it always gets the most recent entry, in case they are added out of order for whatever reason. I have also used this column to correctly plot data in chronological order with ease. Should this evolve into a data science project, this column will be very useful for correctly ordering data. Furthermore, I worked with data from 30 minute intervals for this project. If I were to work with other time intervals, I believe it would be justifiable to create more tables.
* **rain_data.db**  
This is a sqlite3 database containing all the data the bot collects. I have chosen sqlite3 because it is extremely easy to set up and it dispenses the need to have a server up and running, instead serving sort of as a file to dump data into, but which is easier to handle than a csv file. To be fair, this project as it is would not need a database per say, as it works with just the latest data. But still, if it were ever to work with historical data, this would come in handy.
* **main.py**  
This is the main script file. Running this file will start a python program that will run the bot indefinitely, checking for new data every hour. If the bot ever raises an exception, it will stop to avoid any further harm, and await for human input to begin it again. I think an advancement for this code would be to create a log as well, as this would allow debugging should something bad ever occur.
* **populate_database.py**  
This is a separate script which can be used to collect historical data from the government website. It isn't used by the bot at any moment, but I used it to populate the database with data ranging from 2020 to 2023.
* **plot_data.py**  
This is another separate script, which will select data from the database from a time period and plot it onto a graph for visualization. It's a good way to visualize the trend of the river depth by time.



## Further Context
The city of Rio do Sul has a remarkable location in the state of Santa Catarina, Brazil, as in the heart of the city, two rivers join and form the Rio Itajaí-Açu, a major river which flows more than 270km down the state until it reaches the atlantic ocean.  
This river was paramount to the settling of the land by european migrants in the 19th and 20th century, as it allowed for easy access to fresh water and as well transportation of wood down to the coast.  
The location of Rio do Sul, however, is also threatened by its landscape. When it rains, rainwater from the whole region of the Alto Vale do Itajaí flows into the Itajaí-Açu. The river, in turn, is not wide enough and does not have enough flow to keep up with the downpour at times, and flooding occurs.  
As of February of 2024, the time of writing this file, the author of this project himself has lived through 10 separate floods, of varying intensities, after living for 3 years in this city. In November 2023, Rio do Sul faced its second most extreme flood since 1911 as the river rose 10 meters above its normal measument, in a matter of 12 hours. This was a major blow to the local economy, which, as of the time of writing this file, is still far from recovering.  
The Ximbica bridge, the point of interest in this project, is a very small but very important, less than 10 meter long bridge that connects a major quarter to the highway and to the city center. However, it is also located in perhaps the lowest point of the city - so much so that localized heavy rain will cause it to flood in a matter of minutes, much to the inconvenience of everyone who uses it frequently - the author included - hence the point of this project.  