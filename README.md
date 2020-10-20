# Welcome to CFBot Alpha

This a Facebook Messenger Bot for competitive programming enthusiasts. It can show rating changes real time based on contest phase and codeforces handle with Wit's AI power. It uses Wit's NLP (Natural Language Processing) to process your message and automatically detect what you want to know. Cool, right?

### Bot's Server
The bot server is powered by ~Flask~ Quart framework and hosted on heroku. [Click Here](https://cfbotalpha.herokuapp.com/) to go to the website

<!-- ## Sample Conversation -->

## Bot's Artifical Intelligence
CFBot uses Wit's NLP. It's well trained to recognize your message. Send message in correct format without any unnecessary information to get 100% correct reply.

## Tree Structure
```
|-- cache
|   `-- .gitkeep
|-- controllers
|   |-- api_requests.py
|   |-- cache_controller.py
|   |-- facebook_api.py
|   |-- misc_controller.py
|   |-- processor.py
|   |-- rating_calculator.py
|   `-- rating_change_controller.py
|-- static
|   `-- styles.css
|-- templates
|   |-- help.html
|   `-- index.html
|-- .env
|-- .flaskenv
|-- .gitignore
|-- Procfile
|-- README.md
|-- requirements.txt
|-- runtime.txt
|-- server.py
`-- test.py

4 directories, 20 files

```

 ## Installation

Bash commands to install it in Ubuntu 20.04

 ```
$ pipenv shell
$ pipenv run pip install -r requirements.txt
$ export QUART_APP server

# Set other environment variables

$ quart run

 ```
 
 ## License
 This is under MIT License.
