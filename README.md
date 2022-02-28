# Ramp Wordle

This is the contestant repo for the [Ramp Wordle Challenge](https://content.rampgrowth.com/wordle-challenge).

## How does the challenge work?

On `game day` (after submissions have closed) Ramp will generate several Wordles of varying length. These Wordles need to be solved by services hosted by
contestants. Points are assigned based on how few attempts are made to solve the Wordle. The contestant with the overall best score wins.

The image below illustrates the `game day` process.

<img src="wordle_challenge.jpg" width="600"  alt="Wordle Contestant Flow"/>

* Ramp will create several Wordles of varying length between 4 and 9 letters long (inclusive). These Wordles are chosen at random from custom dictionaries
  hosted at S3 (see the file [config.py](/wordle_contestant/config.py) for the list dictionaries and their relevant S3 locations).
* The id for a Wordle will be sent to each contestant service's `/games` endpoint (hosted on heroku).
* Given the Wordle id the contestant service makes calls to the [Ramp Wordle Service](https://ramp-wordle-server.herokuapp.com/) in order to try and solve the
  Wordle within the given time limit of 5 minutes.
* This process of Wordle generation and solving by contestants will repeat several times.

## How do I participate?

* Register via the Wordle challenge [page](https://content.rampgrowth.com/wordle-challenge).
* Fork this repo and implement the missing parts (ee the section `Development Flow` below for an example of what this process looks like). This service already
  contains the basic code required in order to both receive and authorise a request to the `/games` endpoint. It is up to you to implement the necessary code so
  that a `POST` to the `/games` endpoint is able to determine a given Wordle in as few attempts as possible.
* Host your solution on Heroku (you can use the free tier for this).
* Add your `heroku_app_url` via the Ramp Wordle Server endpoint `PUT /contestants/profile` before the submissions close (this allows us to make a call to your
  heroku service).
* Share your private repo with Ramp's GitLab user [RampDeveloper](https://gitlab.com/RampDeveloper) within 24 hours after the submission date has closed.
* See the T&Cs [here](https://content.rampgrowth.com/wordle-challenge/terms-and-conditions).
* GLHF!

## Setup

1. Clone git repository
    ```shell
    git clone git@gitlab.com:rampagency/wordle-contestant.git
    cd wordle-contestant
    ```

1. Create virtual environment and install requirements
    ```shell
    python3 -m venv wordle-contestant
    pip install -r requirements.txt
    ```

1. Add the API key that you received upon registration to your environment variables:
    ```shell
    API_KEY=<YOUR_API_KEY>
    ```

1. Install [Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

   Verify the installation with:
   ```shell
   heroku --version
   ```

   Login to Heroku:
   ```shell
   heroku login
   ```

   Additional Info:
    - [Install Heroku and deploy](https://devcenter.heroku.com/articles/git)

    - [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

1. Add your API_KEY to your heroku app's `Config Vars`

## Run

Run locally on Heroku

```shell
heroku local
```

Deploy to Heroku (local `master` branch to Heroku's `main` branch)

```shell
git push heroku master:main
```

## Development Flow

Typically, a development process will look as follows (the examples below are code snippets taken from using the interactive [OpenAPI](https://ramp-wordle-server.herokuapp.com/) documentation):

1. Create a new Wordle to solve by posting to `/wordles` (set the timeout to a value that suits you):

```shell
curl -X POST "https://ramp-wordle-server.herokuapp.com/wordles" -H "accept: application/json" -H "X-API-Key: xxxxx" -H "Content-Type: application/json" -d "{\"length\":5,\"timeout\":100}"
```
```json
{
  "timeout": 100,
  "id": 51,
  "created_at": "2022-02-28T12:52:00.114457",
  "length": 5
}
```

2. Attempt to solve the Wordle by making guesses with the endpoint `/attempts` until you get a result where every letter has been found (i.e. it's all `h`s):
```shell
curl -X POST "https://ramp-wordle-server.herokuapp.com/attempts" -H "accept: application/json" -H "X-API-Key: xxxxx" -H "Content-Type: application/json" -d "{\"guess\":\"prize\",\"wordle_id\":51}"
```
```json
{
  "game_id": 23,
  "result": "mmmmm",
  "guess": "prize"
}
```
```shell
curl -X POST "https://ramp-wordle-server.herokuapp.com/attempts" -H "accept: application/json" -H "X-API-Key: xxxxx" -H "Content-Type: application/json" -d "{\"guess\":\"known\",\"wordle_id\":51}"
```
```json
{
  "game_id": 23,
  "result": "hhhhh",
  "guess": "known"
}
```
```shell
curl -X POST "https://ramp-wordle-server.herokuapp.com/attempts" -H "accept: application/json" -H "X-API-Key: xxxxx" -H "Content-Type: application/json" -d "{\"guess\":\"done\",\"wordle_id\":51}"
```
```json
{
  "message": "Wordle already solved"
}
```

The major difference between the development process and the activities on `game day` is that on the `game day` Ramp will be generating the Wordles followed by posting those Wordle IDs to the contestant services (it's up to the contestant service to query the length of the Wordle via the endpoint `/wordles/{wordle_id}`).
