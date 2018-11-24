# What Happened - A Twitter Experiment

This small web app shows what happened in given year or day. 
It also integrates Twitter API to display events that happened at the creation date of given Twitter account.

# Usage
- Clone the repository
- Install the requirements using `pip install -r requirements.txt`
- Run app.py

# API
- `/events/<int:month>/<int:day>`:  
    Returns a JSON list of events at given day & month. Scrapes and parses and returns the corresponding [wiki page][day_wiki]
- `/events/<int:year>`:  
    Returns a JSON list of events that happened in given year. Scrapes and parses and returns the corresponding [wiki page][year_wiki]
- `/events/<string:twitter_handle>`:  
    Returns a JSON object that includes:
    
    - The list of events that happened at creation day, i.e. April 20 throughout the history.
    - The list of events that happened in creation year
    - The creation date of the account
 
[day_wiki]: https://en.wikipedia.org/wiki/April_1
[year_wiki]: https://en.wikipedia.org/wiki/2016