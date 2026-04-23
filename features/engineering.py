import pandas as pd
from pandas import DataFrame
from pathlib import Path


def main():
    # Read data
    df = pd.read_csv(f"{Path(__file__).parent}/../data/hist_data.csv")
    return engineering(df)


def engineering(df: DataFrame):
    # close_lag1..5
    df["close_lag1"] = df["Close"].shift(1)
    df["close_lag2"] = df["Close"].shift(2)
    df["close_lag3"] = df["Close"].shift(3)
    df["close_lag4"] = df["Close"].shift(4)
    df["close_lag5"] = df["Close"].shift(5)

    # return_1d
    df["return_1d"] = df["Close"].pct_change()
    # df["return_1d"] = (df["Close"] - df["Close"].shift(1)) / df["Close"].shift(1)
    
    # volume_ma5
    df["volume_ma5"] = df["Volume"].rolling(window=5).mean()

    # rsi_14
    diff = df["Close"].diff()
    gain = diff.clip(lower=0)
    loss = (-diff).clip(lower=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    # target
    df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    return df.dropna()


if __name__ == '__main__':
    df = main()
    print(df.head())
    print(df.shape)