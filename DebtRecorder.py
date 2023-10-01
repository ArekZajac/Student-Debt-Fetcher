import sqlite3
from datetime import datetime, timedelta
from DebtFetcher import DebtFetcher

class DebtRecorder():
    def __init__(self) -> None:
        self.conn = sqlite3.connect("DebtRecords.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                debt FLOAT NOT NULL,
                rate FLOAT NOT NULL
                )""")
        self.cur.execute("""
                CREATE TABLE IF NOT EXISTS forecast (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                debt FLOAT NOT NULL,
                rate FLOAT NOT NULL
                )""")

    def record_data(self):
        debt_fetcher = DebtFetcher()
        debt, rate, asof = debt_fetcher.get_debt_info()

        # Convert asof from string to date
        asof_date = datetime.strptime(asof, "%d %B %Y")

        # Find if last entry in history table is older than the one fetched above
        self.cur.execute("SELECT MAX(date) FROM history")
        last_entry_date = self.cur.fetchone()[0]
        if last_entry_date is not None:
            last_entry_date = datetime.strptime(last_entry_date, "%Y-%m-%d")

        if last_entry_date is None or last_entry_date < asof_date:
            # If it is, add this entry to the table
            self.cur.execute("INSERT INTO history (date, debt, rate) VALUES (?, ?, ?)", (asof_date.strftime("%Y-%m-%d"), debt, rate))
            self.conn.commit()

            # Use generate_forecast to re-generate daily forecast for next 10 years
            self.generate_forecast()

        # Close the database connection
        self.cur.close()
        self.conn.close()

    def generate_forecast(self):
        # Fetch the last recorded debt and rate values
        self.cur.execute("SELECT debt, rate FROM history ORDER BY date DESC LIMIT 1")
        last_debt, last_rate = self.cur.fetchone()

        # Clear the existing forecast table
        self.cur.execute("DELETE FROM forecast")
        self.conn.commit()

        # Generate daily forecast for next 10 years and put the data into forecast table
        today = datetime.today().date()
        for day in range(365 * 10):  # 10 years of days
            forecast_date = today + timedelta(days=day)
            daily_increase = (last_rate / 365) * last_debt
            forecast_debt = last_debt + (daily_increase * day)
            self.cur.execute("INSERT INTO forecast (date, debt, rate) VALUES (?, ?, ?)", (forecast_date.strftime("%Y-%m-%d"), forecast_debt, last_rate))
        self.conn.commit()

if __name__ == "__main__":
    recorder = DebtRecorder()
    recorder.record_data()
