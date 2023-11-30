# Student Debt Fetcher

Tired of living a stress free life, ignorant of the student debt looming over your head? Use this mini web scraper to easily fetch how much you owe the country!

Since the UK Government does not provide an API to get your amount of debt, this tool utilizes Selenium to log into your account and read the amount that the website shows. This can be accessed by running the `DebtFetcher.py` script, or via a REST API by hosting the `APIServer.py`.

## Prerequisites
1. Run `pip install -r requirements.txt` in the project directory to ensure all dependencies are satisfied.

This will install the following libraries:
- fastapi
- python-dotenv
- selenium

### Run Locally
1. Duplicate or rename the `.env-template` file to `.env`.
2. In the `.env` file, fill in the `USERNAME`, `PASSWORD`, and `SECRET` variables to match the ones you use to log in.
3. Keep the `HEADLESS` value to `True` to run the tool without a web browser popping up, setting it to `False` will allow you to see it's work in action.
4. Running `python main.py` will result in the debt value getting printed into your console. If the file is imported, calling `GetDebt()` will return the debt value.

### Host API
1. Run `pip install uvicorn` to install the API web server.
2. Run `uvicorn APIServer:api --reload` to start the web server.
3. Request `GET /debtinfo?username={username}&password={password}&secret={secret}`
4. The 200 response will be `{"debt": float, "rate": float, "updated": str}`.
5. If the login details provided are incorrect, a 500 response will be returned.