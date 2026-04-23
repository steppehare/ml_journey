import yfinance as yf
from pathlib import Path


def main():
    hist_data = yf.download(
        "EURUSD=X",
        start="2023-01-01",
        end="2026-01-01",
        interval="1d",
        auto_adjust=True
    )
    hist_data.columns = hist_data.columns.get_level_values(0)  # leave only column with headers
    hist_data.to_csv(Path(__file__).parent / "hist_data.csv")


if __name__ == "__main__":
    main()
