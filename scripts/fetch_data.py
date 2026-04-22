import yfinance as yf
import sqlite3
import pandas as pd
from pathlib import Path

# Point to the data folder to create market_data db file
db_path = Path(__file__).resolve().parents[1]/"data"/"market_data.db"


tickers=["MSFT", "AAPL", "GOOGL"]
start="2022-01-01"
end="2026-01-01"


# df = yf.download("MSFT", start=start, end=end, auto_adjust=True)
# df.columns = df.columns.get_level_values(0)
# print(df.columns)




def fetch_and_store(tickers: list[str], start:str, end:str) -> None:
    con = sqlite3.connect(db_path)

    for ticker in tickers:
        print(f"Fetching {ticker}...")
        df = yf.download(ticker, start=start, end=end, auto_adjust=True)
        df.columns = df.columns.get_level_values(0)
        df.index.name = "date"
        df["ticker"] = ticker
        df.reset_index(inplace=True)

        df.to_sql("market_data_for_time_series", con, if_exists='append', index=False)
        print(f"Stored {len(df)} rows to database table")

    con.execute("""
        CREATE TABLE IF NOT EXISTS market_data_for_time_series_clean AS
        SELECT DISTINCT  * FROM market_data_for_time_series
    """)
    con.commit()
    con.close()
    print(f"Creation complete. DB saved to {db_path}")


if __name__ == "__main__":
    fetch_and_store(tickers, start, end)
