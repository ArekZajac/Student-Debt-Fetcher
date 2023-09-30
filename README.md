# Student Debt Fetcher

Tired of living a stress free life, ignorant of the student debt looming over your head? Use this mini web scraper to easily fetch how much you owe the country!

Since the UK Government does not provide an API to get your amount of debt, this tool utilizes Selenium to log into your account and read the amount that the website shows.

## Prerequisites
- Python 3
- Pip

## Usage
1. Duplicate or rename the `.env-template` file to `.env`.
2. In the `.env` file, fill in the `USERNAME`, `PASSWORD`, and `SECRET` variables to match the ones you use to log in.
3. Keep the `HEADLESS` value to `True` to run the tool without a web browser popping up, setting it to `False` will allow you to see it's work in action.
4. Run `pip install -r requirements.txt` in the project directory to ensure all dependencies are satisfied.
5. Running `python main.py` will result in the debt value getting printed into your console. If the file is imported, calling `GetDebt()` will return the debt value.