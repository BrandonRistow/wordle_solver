import requests
import pandas as pd


def wordle_length(wordle_id):
    """
    Calls the wordle api and gets the length of the wordle based on the wordle ID

    param wordle_id: The wordle ID of the api

    returns str
    """
    url = "https://ramp-wordle-server.herokuapp.com/wordles/" + str(wordle_id)
    headers = {'accept': 'application/json',
               'X-API-Key': "08fc77b5-748b-44e4-8d36-ed95d0257b2f",
               "Content-Type": "application/json"
               }
    res = requests.get(url, headers=headers)

    return res.json()['length']


def start_wordle(length, timeout=1000):
    """
    Generates a random wordle ID from the api

    param length: The length of the wordle
    param timeout: The duration of the wordle challenge

    returns str
    """
    url = "https://ramp-wordle-server.herokuapp.com/wordles"
    headers = {'accept': 'application/json',
               'X-API-Key': "08fc77b5-748b-44e4-8d36-ed95d0257b2f",
               "Content-Type": "application/json"
               }
    j = {'length': str(length), 'timeout': timeout}
    res = requests.post(url,
                        headers=headers,
                        json=j)

    return res.json()['id']


def guess_wordle(wordle_id, guess):
    """
    The post request which submits a wordle guess to the api.

    param wordle_id: The wordle ID of the api
    param guess: The word being submitted as a guess

    returns str
    """
    print('guess = ', guess)
    url = "https://ramp-wordle-server.herokuapp.com/attempts"
    headers = {'accept': 'application/json',
               'X-API-Key': "08fc77b5-748b-44e4-8d36-ed95d0257b2f",
               "Content-Type": "application/json"
               }
    j = {'guess': guess, 'wordle_id': wordle_id}
    g = requests.post(url,
                      headers=headers,
                      json=j)
    try:
        return g.json()['result']
    except KeyError:
        return g.json()['message']


def filter_results(words, guess, result, logging=True):
    """
    Processes a wordle guess over each letter according to whether it was a green, yellow or black result

    words: database of applicable words
    guess: The guessed word
    result: The result of the guess
    logging: Whether to print out the process or not

    returns filtered words database
    """
    for i in range(len(result)):  # Go through each letter and act accordingly
        if result[i] == 'h':  # ie Green
            words = words[words.Words.str[i] == guess[i]]  # filter to just words with that letter in that spot
            if logging:
                print("Letter '" + guess[i] + "'", ' is green in position', i + 1, ": ", len(words),
                      "Possible words remaining")
        elif result[i] == 'f':  # ie yellow
            words = words[words.Words.str.contains(guess[i]) == True]  # Filter to only words with this letter
            words = words[words.Words.str[i] != guess[i]]  # filter out all words with that letter in that spot
            if logging:
                print("Letter '" + guess[i] + "'", ' is yellow in position', i + 1, ": ", len(words),
                      "Possible words remaining")
        else:  # ie black
            for j in range(len(result)):  # Go through each letter
                if guess[j] == guess[i] and result[j] != 'm':
                    pass
                else:
                    words = words[
                        words.Words.str[j] != guess[i]]  # filter out all words with that letter in that spot
            if logging:
                print("Letter '" + guess[i] + "'", ' is black in position', i + 1, ": ", len(words),
                      "Possible words remaining")

    return words


def green_word_scoring(words, guess_round):
    """
    Takes the remaining words and establishes how often each letter appears in each position, that frequency is
    the score given to each letter of each word, with the word providing the highest score being the output

    words: database of words
    guess_round: How many guesses have been made previously

    returns string of the highest scoring word in terms of greens
    """
    wm = words[['Words']].copy()

    heat = pd.DataFrame()
    for i in range(len(wm['Words'].iloc[0])):
        wm['Letter' + str(i + 1)] = wm.Words.str[i]
        gb = wm.groupby('Letter' + str(i + 1)).count()[['Words']].sort_values('Words', ascending=False)
        gb.rename(columns={'Words': 'L' + str(i + 1)}, inplace=True)
        heat = gb.join(heat, how='outer')

    wm['Total'] = 0
    for l in range(len(wm['Words'].iloc[0])):
        wm = wm.join(heat[['L' + str(l + 1)]], on='Letter' + str(l + 1))
        wm['Total'] = wm['Total'] + wm['L' + str(l + 1)]

    if guess_round <= 1:
        try:
            wm = remove_repeat_letters(wm)
        except IndexError:
            pass

    wm = wm[wm.Total == wm.Total.max()]

    return wm['Words'].iloc[0]


def remove_repeat_letters(df):
    """
    Finds all words with repeated letters and filters them out.

    param df: Pandas dataframe of all the available words

    returns Pandas.DataFrame
    """
    x = df.copy()
    for j in range(len(x.Words.iloc[0])):
        for k in range(len(x.Words.iloc[0])):
            if j != k:
                x = x[x['Letter' + str(k + 1)] != x['Letter' + str(j + 1)]]

    return x


def wordle_iteration(words, i, wordle_id, logging=True):
    """
    Performs a single round of a wordle guess

    param words: pandas database of all available words
    param i: The guessing round
    param wordle_id: The wordle ID provided by the api
    param logging: Whether to print out the process or not

    returns pandas.DataFrame, str
    """
    guess = green_word_scoring(words, i)
    result = guess_wordle(wordle_id, guess)
    print(result)
    if result == "Wordle already solved":
        return words, result
    words = filter_results(words, guess, result, logging=logging)

    return words, result


def do_wordle(wordle_id, logging=True):
    """
    Solves for a given wordle

    param wordle_id: The ID of the wordle given by the api
    param logging: Whether to print out the process or not

    returns str
    """
    print('wordle_id:', wordle_id)
    length = wordle_length(wordle_id)
    print('Wordle length: ', length)
    words = pd.read_csv("https://ramp-python-challenge.s3.eu-west-1.amazonaws.com/wordle_" + str(length) + ".csv",
                        names=['Words'])
    for i in range(10):
        words, result = wordle_iteration(words, i, wordle_id, logging=logging)
        if result == "Wordle already solved":
            return result

    return 'Wordle not solved in time'


def run_game(wordle_id):
    """
    Run game.

    You can fetch your API_KEY and a set of dictionaries with
    various word lengths for solving wordles from wordle_contestant.config

    :param wordle_id: Contains the ID of the wordle that needs to be solved
    """
    do_wordle(wordle_id)
