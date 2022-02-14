# Ramp Wordle

## API Docs

API docs can be viewed at: https://ramp-wordle-server.herokuapp.com/

## Setup

1. Clone git repository
    ```shell
    git clone git@gitlab.com:rampagency/wordle-contestant.git
    cd wordle-contestant
    ```

2. Create virtual environment and install requirements
    ```shell
    python3 -m venv wordle-contestant
    pip install -r requirements.txt
    ```

3. API key

    - Register via `/contestants` API and save your API key because you will need it later.
    
    - Add API key to environment variables:
    ```dotenv
    API_KEY=<YOUR_API_KEY>
    ```

4. Install Heroku

    Install: [Heroku Command Line Interface](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

    Verify installation:
    ```bash
    heroku --version
    ```
    
    Login to Heroku:
    ```bash
    heroku login
    ```
    
    Additional info:
    
    - [Install Heroku and deploy](https://devcenter.heroku.com/articles/git)
    
    - [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)


## Run

Run locally on Heroku
```shell
heroku local
```

Deploy to Heroku (local `master` branch to Heroku's `main` branch)
```shell
git push heroku master:main
```
