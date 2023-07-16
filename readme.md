# AFEX-SEARCH-ENGINE

This project is built on Python 3.9.x and Django 4.x.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```
## Setup

Copy the values from the example.env file to a new .env file in the same directory. You can edit the values to suite your credentials.

## Usage

CD into the searchengine folder that contains the manage.py

Run ```bash python manage.py runserver```

This will take approximately 2 minutes on the initial run depending on your network/signal strength. The process of downloading a vital package [nltk_punkt](https://www.nltk.org/_modules/nltk/tokenize/punkt.html) is run once at the beginning of this process. Subsequent server runs on the same system will not require this process.

Visit [Search](http://127.0.0.1:8000) to run a search query.

Visit [Index](http://127.0.0.1:8000/index) to save a document string to DB.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.