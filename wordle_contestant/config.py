import os

# You need to setup your `API_KEY` as environment variable.
API_KEY = os.getenv("API_KEY")

# Use these dictionaries to find the wordle
DICTIONARIES = {
    "4": "https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_4.csv",
    "5": "https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_5.csv",
    "6": "https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_6.csv",
    "7": "https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_7.csv",
    "8": "https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_8.csv",
    "9": "https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_9.csv"
}
